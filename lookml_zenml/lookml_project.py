import re
import os
import lkml
import json
from ruamel.yaml import YAML
import uuid
from collections import defaultdict
from typing import Dict, Any, List

from lookml_zenml.lookml_models import (
    LookMLProject,
    LookMLModel,
    LookMLView,
    LookMLJoin,
    LookMLExplore,
    LookMLDashboard,
    LookMLDimension,
    LookMLDimensionGroup,
    LookMLMeasure,
    LookMLDashboardElement,
    fields_to_replace,
)

FIELD_KEY_ORDER = ["name", "field_type", "type", "description", "timeframes", "sql"]
UNSUPPORTED_MEASURE_TYPES = [
    "date",
    "date_time",
    "list",
    "median_distinct",
    "percent_of_previous",
    "percent_of_total",
    "percentile_distinct",
    "running_total",
    "period_over_period",
    "yesno",
    "int",
]
UNSUPPORTED_DIMENSION_TYPES = ["zipcode"]
UNSUPPORTED_DIMENSION_GROUP_TYPES = ["date", "datetime"]
yaml = YAML()
yaml.indent(sequence=4, offset=2)
yaml.preserve_quotes = False
yaml.default_style = None


# Configure YAML to use literal block scalars for multiline strings
def represent_str(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.representer.add_representer(str, represent_str)


class LookMLProjectConverter:
    def __init__(self, in_directory: str = None, out_directory: str = None):
        self.in_directory = in_directory
        self.out_directory = out_directory
        self.field_mappings = []
        self._views = []
        self._models = []
        self._explore_from_mapping = {}
        self._default_model_name = None

    def convert(self):
        if not self.in_directory:
            raise ValueError(
                "You must pass the in_directory argument to the class to use this function. "
                "If you want to convert dict -> dict use the convert_project function in this class"
            )
        lookml_project = self.load(self.in_directory)
        models, views, dashboards, topics = self.convert_project(lookml_project)

        if not self.out_directory:
            raise ValueError(
                "You must pass the out_directory argument to the class to use this function. "
                "If you want to convert dict -> dict use the convert_project function in this class"
            )
        self.dump(self.out_directory, models, views, dashboards, topics)

    def convert_project(self, lookml_project_dict: dict):
        """Convert a raw LookML project dictionary to ZenML format with type validation."""
        models, views, dashboards, topics = [], [], [], []
        view_metadata = {}
        views_to_models = {}

        # Initialize and validate LookML project structure
        try:
            lookml_project = LookMLProject.from_dict(lookml_project_dict)
            # print("Successfully validated complete LookML project structure")
        except Exception as e:
            print(f"Warning: Could not validate full project structure: {e}")
            raise e

        # Process models with validation
        for model_object in lookml_project.models:
            model = self.convert_model(model_object, generate_view_metadata=True)

            model_view_metadata = model.pop("view_metadata", {})
            self._explore_from_mapping[model["name"]] = model_view_metadata["explore_from_mapping"]
            view_metadata.update(model_view_metadata["graph"])
            for view_name in set(model_view_metadata["graph"].keys()):
                views_to_models[view_name] = model["name"]
            models.append(model)

            # Process topics (explores) from each model
            for explore_object in model_object.explores:
                topic = self.convert_topic(explore_object, model["name"])
                topics.append(topic)

        self._models = models

        self._default_model_name = models[0]["name"]
        for view_object in lookml_project.views:
            view = self.convert_view(
                view_object,
                views_to_models.get(view_object.name, self._default_model_name),
                access_filters=[],
                joins=view_metadata.get(view_object.name, []),
            )
            views.append(view)

        self._views = views

        # Process dashboards with validation
        for dashboard_object in lookml_project.dashboards:
            dashboard = self.convert_dashboard(dashboard_object)
            dashboards.append(dashboard)

        return models, views, dashboards, topics

    @staticmethod
    def convert_model(model_object: LookMLModel, generate_view_metadata: bool = False):
        """Convert a LookML model to a ZenML model
        Args: model (dict): A LookML model
              generate_view_metadata (bool): Whether to generate view metadata
                                                based on the explores in the model
        Returns: dict: A ZenML model (if generate_view_metadata is False) or a ZenML
                        with the extra key 'view_metadata' (if generate_view_metadata is True)
        """
        try:
            model_yaml = {
                "version": 1,
                "type": "model",
                "name": model_object.name,
                "connection": model_object.connection,
            }
        except KeyError as e:
            raise KeyError(
                f"The LookML model is missing a required key: {e}. Please check your model and try again."
            )
        if model_object.label:
            model_yaml["label"] = model_object.label
        if model_object.access_grants:
            model_yaml["access_grants"] = [ag.model_dump() for ag in model_object.access_grants]
        if model_object.week_start_day:
            model_yaml["week_start_day"] = model_object.week_start_day.lower()

        if generate_view_metadata:
            model_yaml["view_metadata"] = LookMLProjectConverter.get_view_metadata(model_object)
        return model_yaml

    @staticmethod
    def parse_sql_on(sql_on: str):
        # This code parses a sql_on to determine the relationship between two views
        remaining_sql = sql_on
        references = LookMLProjectConverter.fields_to_replace(sql_on)
        for field in references:
            remaining_sql = remaining_sql.replace(f"${{{field}}}", "")

        # Iff this is true then the sql_on is really just comparing two fields to each other
        if remaining_sql.strip() == "=":
            return "identifier", references

        # Otherwise we need to assume the sql_on is custom
        return "custom", references

    def parse_join(join: LookMLJoin):
        if join.sql_on:
            return LookMLProjectConverter.parse_sql_on(join.sql_on)
        else:
            print(f'Skipping join {join} without "sql_on"')

    @staticmethod
    def get_view_metadata(model: LookMLModel) -> dict:

        explore_from_mapping: Dict[str, Dict[str, str]] = defaultdict(dict)
        identifier_graph: Dict[str, Dict[str, List[Dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
        for explore in model.explores:
            if explore.from_:
                explore_from_mapping[explore.name][explore.name] = explore.from_.name
            else:
                explore_from_mapping[explore.name][explore.name] = explore.name

            root_view = explore_from_mapping[explore.name][explore.name]
            for join in explore.joins:
                if join.from_:
                    explore_from_mapping[explore.name][join.name] = join.from_
                pair_id = str(uuid.uuid4())
                join_view = join.name if not join.from_ else join.from_

                # Relationship always corresponds to the root view in the explore
                # many_to_one is the default join type
                relationship = join.relationship or "many_to_one"
                join_type, references = LookMLProjectConverter.parse_join(join)

                # If the relationship is one_to_one then we can assume that the
                # key's used in the join are unique (primary) in both views
                if relationship == "one_to_one":
                    if join_type == "identifier":
                        for reference in references:
                            view_name, field_name = reference.split(".")
                            if view_name in explore_from_mapping[explore.name]:
                                view_name = explore_from_mapping[explore.name][view_name]
                            identifier = LookMLProjectConverter._to_identifier(field_name, "primary", pair_id)
                            identifier_graph[view_name][identifier["sql"]].append(identifier)

                # If the relationship is one_to_many then we can assume that the
                # key's used in the join are unique (primary) ONLY if the key references the root view
                elif relationship == "one_to_many":
                    if join_type == "identifier":
                        for reference in references:
                            view_name, field_name = reference.split(".")
                            if view_name == root_view:
                                identifier = LookMLProjectConverter._to_identifier(
                                    field_name, "primary", pair_id
                                )
                            else:
                                identifier = LookMLProjectConverter._to_identifier(
                                    field_name, "foreign", pair_id
                                )
                            if view_name in explore_from_mapping[explore.name]:
                                view_name = explore_from_mapping[explore.name][view_name]
                            identifier_graph[view_name][identifier["sql"]].append(identifier)

                # We do not want to replicate many_to_many joins since they get out of hand quickly
                elif relationship == "many_to_many":
                    pass

                # If the relationship is many_to_one then we can assume that the
                # key's used in the join are unique (primary) ONLY if the key references the join view
                elif relationship == "many_to_one":
                    if join_type == "identifier":
                        for reference in references:
                            view_name, field_name = reference.split(".")
                            if view_name in explore_from_mapping[explore.name]:
                                view_name = explore_from_mapping[explore.name][view_name]
                            if view_name == join_view:
                                identifier = LookMLProjectConverter._to_identifier(
                                    field_name, "primary", pair_id
                                )
                            else:
                                identifier = LookMLProjectConverter._to_identifier(
                                    field_name, "foreign", pair_id
                                )
                            identifier_graph[view_name][identifier["sql"]].append(identifier)
                else:
                    raise NotImplementedError(f"Relationship {relationship} is not supported")

        resolved_id_graph, pairs_resolved = defaultdict(list), []
        for view_name, graph in identifier_graph.items():
            for _, identifiers in graph.items():
                names, view_types, view_sql = [], defaultdict(list), defaultdict(list)

                # Loop through identifiers unique on view -> sql and then find the
                # associated pair to connect for the right naming
                for identifier in identifiers:
                    pair_id = identifier["pair_id"]
                    views, ids = LookMLProjectConverter._get_pair(pair_id, identifier_graph)
                    for v, i in zip(views, ids):
                        if i["pair_id"] not in pairs_resolved:
                            names.append(i["name"])
                            view_types[v].append(i["type"])
                            view_sql[v].append(i["sql"])

                # Mark pairs as resolved
                pairs_resolved.extend(list(set(identifier["pair_id"] for identifier in identifiers)))

                # Names need to match across all identifiers, so we find the longest name in
                # the set of potentially joinable ids and use that name across all of them
                if names:
                    longest_name = max(names, key=len)
                    derived_view_identifier_types = {
                        v: "primary" if "primary" in types else "foreign" for v, types in view_types.items()
                    }
                    derived_view_sql = {v: list(set(sql))[0] for v, sql in view_sql.items()}
                    for view in derived_view_identifier_types.keys():
                        identifier = {
                            "name": longest_name,
                            "type": derived_view_identifier_types[view],
                            "sql": derived_view_sql[view],
                        }
                        if identifier not in resolved_id_graph[view]:
                            resolved_id_graph[view].append(identifier)

        return {"graph": resolved_id_graph, "explore_from_mapping": explore_from_mapping}

    @staticmethod
    def _get_pair(pair_id, id_graph):
        views, ids = [], []
        for view_name, graph in id_graph.items():
            for _, identifiers in graph.items():
                for identifier in identifiers:
                    if identifier["pair_id"] == pair_id:
                        views.append(view_name)
                        ids.append(identifier)
        return views, ids

    @staticmethod
    def convert_view(view: LookMLView, model_name: str, access_filters: list = [], joins: list = []):
        zenml_view = {
            "version": 1,
            "type": "view",
            "name": view.name,
            "model_name": model_name,
            "required_access_grants": view.required_access_grants,
            "sets": [s.model_dump() for s in view.sets],
            "access_filters": [af.model_dump() for af in access_filters],
            "identifiers": joins,
        }

        if view.view_label:
            zenml_view["label"] = view.view_label

        if view.description:
            zenml_view["description"] = view.description

        if view.sql_table_name:
            zenml_view["sql_table_name"] = view.sql_table_name

        if view.derived_table:
            # Convert literal \n characters to actual newlines for better YAML formatting
            sql_content = view.derived_table.sql.replace("\\n", "\n")
            zenml_view["derived_table"] = {"sql": sql_content}

        dimensions = [
            f for field in view.dimensions if (f := LookMLProjectConverter.convert_dimension(field))
        ]
        dimension_groups = [
            f
            for field in view.dimension_groups
            if (f := LookMLProjectConverter.convert_dimension_group(field))
        ]
        view_primary_key = next((f["name"] for f in dimensions if f.get("primary_key", False)), None)
        if view_primary_key:
            view_primary_key = view.name + "." + view_primary_key
        measures = [
            f
            for field in view.measures
            if (f := LookMLProjectConverter.convert_measure(field, view_primary_key))
        ]

        fields = dimensions + dimension_groups + measures

        first_date_field = next((f["name"] for f in fields if f["field_type"] == "dimension_group"), None)
        if first_date_field:
            zenml_view["default_date"] = first_date_field

        zenml_view["fields"] = fields

        return zenml_view

    def convert_dashboard(self, dashboard_object: LookMLDashboard):
        zenml_data = {
            "version": 1,
            "type": "dashboard",
            "name": dashboard_object.dashboard,
            "label": dashboard_object.title,
            "elements": [],
        }
        if dashboard_object.description:
            zenml_data["description"] = dashboard_object.description

        if dashboard_object.filters:
            zenml_data["filters"] = []
            for f in dashboard_object.filters:
                field = self._get_field(f.field, self._views, model_name=f.model, explore_name=f.explore)
                default_value = f.default_value
                if default_value == "No":
                    default_value = False
                elif default_value == "Yes":
                    default_value = True
                zenml_data["filters"].append({"name": f.name, "field": field["id"], "value": default_value})

        sorted_elements = sorted(dashboard_object.elements, key=lambda x: (x.row, x.col))
        for element in sorted_elements:
            zenml_element = self._translate_dashboard_element(element)
            if zenml_element:
                zenml_data["elements"].append(zenml_element)

        return zenml_data

    def _translate_dashboard_element(self, element: LookMLDashboardElement):
        if element.merged_queries:
            return self._translate_merged_queries_element(element)
        return self._translate_vanilla_element(element)

    def _translate_vanilla_element(self, element: LookMLDashboardElement):
        # We do not support conditional formatting in dashboards
        if not element.model and element.type not in {"button", "text"}:
            return None

        elif element.type == "text":
            model_name = self._default_model_name if self._default_model_name else "todo"
            zenml_element = {"model": model_name, "type": "markdown", "size": "quarter"}
            zenml_element["content"] = element.body_text
            return zenml_element

        elif element.type == "button":
            model_name = self._default_model_name if self._default_model_name else "todo"
            zenml_element = {"model": model_name, "type": "markdown", "size": "quarter"}
            content_json = json.loads(element.rich_content_json)
            link_url = content_json.get("href", "")

            if link_text := content_json.get("text", ""):
                content = f"[{link_text}]({link_url})"
            else:
                content = link_url

            zenml_element["content"] = content
            return zenml_element

        zenml_element = {"model": element.model, "metrics": [], "slice_by": []}
        if element.title:
            zenml_element["title"] = element.title

        # Add fields
        if not element.fields:
            return None

        for f in element.fields:
            field = self._get_field(f, self._views, model_name=element.model, explore_name=element.explore)
            if field["field_type"] == "measure":
                zenml_element["metrics"].append(field["id"])
            else:
                zenml_element["slice_by"].append(field["id"])

        if element.pivots:
            zenml_element["pivot_by"] = []
            for p in element.pivots:
                field = self._get_field(
                    p, self._views, model_name=element.model, explore_name=element.explore
                )
                zenml_element["pivot_by"].append(field["id"])

        if element.filters:
            zenml_element["filters"] = []
            for k, v in element.filters.items():
                field = self._get_field(
                    k, self._views, model_name=element.model, explore_name=element.explore
                )
                if v != "":
                    if v == "No":
                        v = False
                    elif v == "Yes":
                        v = True
                    zenml_element["filters"].append({"field": field["id"].lower(), "value": v})

        if element.listen:
            zenml_element["listen"] = element.listen

        if element.sorts:
            zenml_element["sort"] = []
            for sort_str in element.sorts:
                split_str = sort_str.split(" ")
                field = self._get_field(
                    split_str[0],
                    self._views,
                    model_name=element.model,
                    explore_name=element.explore,
                )
                if len(split_str) == 1:
                    zenml_element["sort"].append({"field": field["id"].lower(), "value": "asc"})
                else:
                    zenml_element["sort"].append(
                        {"field": field["id"].lower(), "value": split_str[1].lower()}
                    )

        if element.width:
            relative_width = float(element.width) / 24
            if relative_width > 0.5:
                zenml_element["size"] = "full"
            elif relative_width > 0.25:
                zenml_element["size"] = "half"
            else:
                zenml_element["size"] = "quarter"

        if element.show_totals:
            zenml_element["show_totals"] = bool(element.show_totals)

        if element.show_value_labels is not None:
            zenml_element["show_annotations"] = bool(element.show_value_labels)

        if element.limit:
            zenml_element["row_limit"] = element.limit

        if element.dynamic_fields:
            zenml_element["table_calculations"] = []
            for dynamic_field in element.dynamic_fields:
                # We do not currently support dynamic fields that are not table calculations
                if dynamic_field.get("category") == "table_calculation" and not dynamic_field.get(
                    "is_disabled", False
                ):
                    zenml_element["table_calculations"].append(
                        {
                            "title": dynamic_field["label"],
                            "formula": self._clean_table_calc(dynamic_field["expression"], element=element),
                            "format": dynamic_field.get("value_format_name", "decimal_1"),
                        }
                    )

        plot_lookup = {
            "looker_area": "area",
            "looker_donut_multiples": "donut",
            "looker_bar": "horizontal_bar",
            "looker_pie": "pie",
            "table": "table_only",
            "looker_scatter": "scatter",
            "single_value": "stat_plot",
        }

        if element.type == "looker_column":
            plot = "grouped_bar" if len(zenml_element["slice_by"]) > 1 else "bar"
            if element.stacking == "normal":
                plot_options = {"grouped_bar": {"display_type": "STACKED"}}
                zenml_element["plot_options"] = plot_options
            zenml_element["plot_type"] = plot
        elif element.type == "looker_line":
            "line" or "multi_line"
            plot = "multi_line" if len(zenml_element["slice_by"]) > 1 else "line"
            zenml_element["plot_type"] = plot
        elif element.type in plot_lookup:
            zenml_element["plot_type"] = plot_lookup[element.type]
            if zenml_element["plot_type"] == "table_only":
                zenml_element["force_table"] = True

        return zenml_element

    def _get_field(self, field_id: str, views: list, model_name: str = None, explore_name: str = None):
        if len(field_id.split(".")) == 2 and model_name and explore_name:
            explore_view_name, field_name = field_id.split(".")
            if explore_view_name in self._explore_from_mapping.get(model_name, {}).get(explore_name, {}):
                explore_view_name = self._explore_from_mapping[model_name][explore_name][explore_view_name]
            field_id = f"{explore_view_name}.{field_name}"

        for v in views:
            for f in v["fields"]:
                if f"{v['name']}.{f['name']}" == field_id.lower() and f["field_type"] != "dimension_group":
                    return {**f, "id": field_id}
                elif f"{v['name']}.{f['name']}" in field_id.lower() and f["field_type"] == "dimension_group":
                    return {**f, "id": field_id}
        # If we can't find the field assume it will be a dimension on a dashboard
        return {"field_type": "dimension", "id": field_id}

    def _clean_table_calc(self, formula: str, element: LookMLDashboardElement):
        for field_to_replace in self.fields_to_replace(formula):
            if ":row_total" in field_to_replace:
                field_id = field_to_replace.split(":row_total")[0]
                field = self._get_field(
                    field_id,
                    self._views,
                    model_name=element.model,
                    explore_name=element.explore,
                )
                formula = formula.replace(f"${{{field_to_replace}}}", f"sum([{field['id']}])")
            else:
                field = self._get_field(
                    field_to_replace,
                    self._views,
                    model_name=element.model,
                    explore_name=element.explore,
                )
                formula = formula.replace(f"${{{field_to_replace}}}", f"[{field['id']}]")
        return formula

    def _translate_merged_queries_element(self, element: LookMLDashboardElement):
        # We do not support translation for looker filter expressions

        filters_by_expression = defaultdict(list)
        for merged in element.merged_queries:
            if "join_fields" in merged:
                for join_field in merged["join_fields"]:
                    self.field_mappings.append([join_field["field_name"], join_field["source_field_name"]])
            if "filters" in merged:
                for f, e in merged["filters"].items():
                    filters_by_expression[e].append(f)

        for filter_fields in filters_by_expression.values():
            if len(filter_fields) > 1:
                self.field_mappings.append([filter_fields[0], filter_fields[1]])

        running_fields = []
        for merged in element.merged_queries:
            for f in merged["fields"]:
                # Add fields that are not mappings
                matched_pair = next((pair for pair in self.field_mappings if f in pair), None)

                # We can add one and only one field from the mappings to the running fields
                if matched_pair and all(p not in running_fields for p in matched_pair):
                    running_fields.append(f)

                # We can always add fields that are not in the mappings at all
                if all(f not in pair for pair in self.field_mappings):
                    running_fields.append(f)

        first_element = element.merged_queries[0]
        first_element["name"] = element.name
        first_element["fields"] = running_fields

        return self._translate_vanilla_element(LookMLDashboardElement.from_dict(first_element))

    @staticmethod
    def fields_to_replace(text: str):
        return fields_to_replace(text)

    def load(self, in_directory: str):
        lookml = {"views": [], "models": [], "dashboards": []}
        for root, _, files in os.walk(in_directory):
            for file in files:
                if self.is_lookml_file(file):
                    lookml_file = os.path.join(root, file)
                    with open(lookml_file) as f:
                        lookml_dict = lkml.load(f)

                    if ".model." in file:
                        lookml_dict["name"] = file.split(".model.")[0]
                        lookml["models"].append(lookml_dict)
                    elif ".view." in file:
                        lookml["views"].extend(lookml_dict["views"])
                    else:
                        raise NotImplementedError(f"File {file} is not a model or view")

                if self.is_lookml_dashboard_file(file):
                    lookml_file = os.path.join(root, file)
                    with open(lookml_file) as f:
                        lookml_dict = yaml.load(f)
                    lookml["dashboards"].extend(lookml_dict)
        return lookml

    @staticmethod
    def dump(out_directory: str, models: list, views: list, dashboards: list, topics: list):
        zenlytic_project = {
            "name": "new_zenlytic_project",
            "profile": "new_zenlytic_project",
            "dashboard-paths": ["dashboards"],
            "view-paths": ["views"],
            "model-paths": ["models"],
            "topic-paths": ["topics"],
        }
        if not os.path.exists(out_directory):
            raise ValueError(f"The output directory you specified, `{out_directory}` does not exist.")

        with open(os.path.join(out_directory, "zenlytic_project.yml"), "w") as f:
            yaml.dump(zenlytic_project, f)

        for directory in ["models", "views", "dashboards", "topics"]:
            fully_qualified_path = os.path.join(out_directory, directory)
            if not os.path.exists(fully_qualified_path):
                os.mkdir(fully_qualified_path)

        for model in models:
            with open(os.path.join(out_directory, f"models/{model['name']}_model.yml"), "w") as f:
                yaml.dump(model, f)

        for view in views:
            with open(os.path.join(out_directory, f"views/{view['name']}_view.yml"), "w") as f:
                yaml.dump(view, f)

        for dashboard in dashboards:
            with open(os.path.join(out_directory, f"dashboards/{dashboard['name']}.yml"), "w") as f:
                yaml.dump(dashboard, f)

        for topic in topics:
            with open(os.path.join(out_directory, f"topics/{topic['name']}_topic.yml"), "w") as f:
                topic.pop("name")
                yaml.dump(topic, f)

    @staticmethod
    def convert_dimension(dimension: LookMLDimension):
        converted = {
            "name": dimension.name,
            "field_type": "dimension",
        }
        if dimension.sql:
            converted["sql"] = dimension.sql.replace("\\n", "\n")
        elif dimension.case:
            converted["case"] = dimension.case
        else:
            converted["sql"] = "${TABLE}." + dimension.name
        if dimension.label:
            converted["label"] = dimension.label
        if dimension.required_access_grants:
            converted["required_access_grants"] = dimension.required_access_grants
        if dimension.group_label:
            converted["group_label"] = dimension.group_label
        if dimension.description:
            converted["description"] = dimension.description
        if dimension.hidden:
            converted["hidden"] = dimension.hidden == "yes"
        if dimension.primary_key:
            converted["primary_key"] = dimension.primary_key == "yes"
        if dimension.tiers:
            converted["tiers"] = [int(tier) for tier in dimension.tiers]
        if dimension.type and dimension.type not in UNSUPPORTED_DIMENSION_TYPES:
            converted["type"] = dimension.type
        else:
            converted["type"] = "string"

        if converted["type"] == "string":
            converted["searchable"] = True

        if dimension.links:
            converted["link"] = dimension.links[0].url

        return LookMLProjectConverter.sort_dict(converted, FIELD_KEY_ORDER)

    @staticmethod
    def convert_dimension_group(dimension_group: LookMLDimensionGroup):
        converted = {"name": dimension_group.name, "field_type": "dimension_group"}
        if dimension_group.label:
            converted["label"] = dimension_group.label
        if dimension_group.description:
            converted["description"] = dimension_group.description
        if dimension_group.group_label:
            converted["group_label"] = dimension_group.group_label
        if dimension_group.required_access_grants:
            converted["required_access_grants"] = dimension_group.required_access_grants
        if dimension_group.type and dimension_group.type not in UNSUPPORTED_DIMENSION_GROUP_TYPES:
            converted["type"] = dimension_group.type
        else:
            converted["type"] = "time"
        if dimension_group.sql:
            converted["sql"] = dimension_group.sql.replace("\\n", "\n")
        if dimension_group.sql_start:
            converted["sql_start"] = dimension_group.sql_start.replace("\\n", "\n")
        if dimension_group.sql_end:
            converted["sql_end"] = dimension_group.sql_end.replace("\\n", "\n")
        if dimension_group.hidden:
            converted["hidden"] = dimension_group.hidden == "yes"
        if dimension_group.primary_key:
            converted["primary_key"] = converted["primary_key"] == "yes"
        if dimension_group.convert_tz:
            converted["convert_tz"] = dimension_group.convert_tz == "yes"
        if dimension_group.convert_timezone:
            converted["convert_timezone"] = dimension_group.convert_timezone == "yes"
        if dimension_group.type == "time" and not dimension_group.timeframes:
            converted["timeframes"] = ["raw", "date", "week", "month", "quarter", "year"]
        if dimension_group.timeframes:
            converted["timeframes"] = dimension_group.timeframes
        if dimension_group.intervals:
            converted["intervals"] = dimension_group.intervals
        elif dimension_group.type == "duration" and not dimension_group.intervals:
            converted["intervals"] = ["day", "week", "month", "quarter", "year"]

        return LookMLProjectConverter.sort_dict(converted, FIELD_KEY_ORDER)

    @staticmethod
    def convert_measure(measure: LookMLMeasure, view_primary_key: str = None):
        # These measure types are not supported in LookML -> ZenML conversion
        if measure.type and measure.type in UNSUPPORTED_MEASURE_TYPES:
            return {}

        if view_primary_key:
            view_primary_key_sql = f"${{{view_primary_key}}}"
        else:
            view_primary_key_sql = "*"

        converted = {
            "name": measure.name,
            "field_type": "measure",
            "sql": measure.sql.replace("\\n", "\n") if measure.sql else view_primary_key_sql,
        }
        if measure.label:
            converted["label"] = measure.label
        if measure.type:
            converted["type"] = measure.type
        if measure.required_access_grants:
            converted["required_access_grants"] = measure.required_access_grants
        if measure.sql_distinct_key:
            converted["sql_distinct_key"] = measure.sql_distinct_key.replace("\\n", "\n")
        if measure.description:
            converted["description"] = measure.description
        if measure.hidden:
            converted["hidden"] = measure.hidden == "yes"
        if measure.percentile:
            converted["percentile"] = measure.percentile
        if measure.group_label:
            converted["group_label"] = measure.group_label

        if measure.value_format_name:
            converted["value_format_name"] = measure.value_format_name

        if measure.filters:
            converted["filters"] = [f.model_dump() for f in measure.filters]

        return LookMLProjectConverter.sort_dict(converted, FIELD_KEY_ORDER)

    @staticmethod
    def convert_topic(explore_object: LookMLExplore, model_name: str):
        """Convert a LookML explore to a ZenML topic."""
        topic = {
            "version": 1,
            "type": "topic",
            "name": explore_object.name,
            "model_name": model_name,
        }

        if explore_object.label:
            topic["label"] = explore_object.label.strip()
        else:
            topic["label"] = explore_object.name.replace("_", " ").title().strip()
        if explore_object.description:
            topic["description"] = explore_object.description
        if explore_object.hidden is not None:
            topic["hidden"] = explore_object.hidden == "yes"
        if explore_object.from_:
            topic["base_view"] = explore_object.from_.name
        elif explore_object.view_name:
            topic["base_view"] = explore_object.view_name
        else:
            topic["base_view"] = explore_object.name
        if explore_object.extends:
            raise NotImplementedError("Extends are not supported in ZenML")

        if explore_object.extension:
            raise NotImplementedError("Extension is not supported in ZenML")

        if explore_object.fields:
            print(
                f"Field restriction is not supported in ZenML in a topic, passing on "
                f"this argument in the explore {explore_object.name}"
            )
        if explore_object.sql_always_where:
            print(
                f"SQL always where is not supported in ZenML, passing on "
                f"this argument in the explore {explore_object.name}"
            )
        if explore_object.required_access_grants:
            topic["required_access_grants"] = explore_object.required_access_grants

        if explore_object.always_filter:
            topic["always_filter"] = explore_object.always_filter.model_dump()["filters"]

        if explore_object.conditionally_filter:
            print(
                f"Conditionally filter is not supported in ZenML, passing on "
                f"this argument in the explore {explore_object.name}"
            )
        if explore_object.access_filter:
            topic["access_filter"] = [af.model_dump() for af in explore_object.access_filter]

        if explore_object.joins:
            topic["views"] = {
                join.name: {
                    "join": {
                        "join_type": join.type or "left_outer",
                        "relationship": join.relationship or "many_to_one",
                        "sql_on": join.sql_on,
                    }
                }
                for join in explore_object.joins
            }

        if explore_object.sql_table_name:
            print(
                f"SQL table name is not supported in ZenML in an explore, passing on "
                f"this argument in the explore {explore_object.name}"
            )

        return topic

    @staticmethod
    def _to_identifier(field_name: str, type: str, pair_id: str):
        return {"name": field_name, "type": type, "sql": f"${{{field_name}}}", "pair_id": pair_id}

    @staticmethod
    def is_lookml_file(file):
        suffixes = [".model.lkml", ".view.lkml", ".model.lookml", ".view.lookml"]
        return any(file.endswith(suffix) for suffix in suffixes)

    @staticmethod
    def is_lookml_dashboard_file(file):
        suffixes = [".dashboard.lkml", ".dashboard.lookml"]
        return any(file.endswith(suffix) for suffix in suffixes)

    @staticmethod
    def sort_dict(d: dict, sort_order: list):
        sorted_dict = {k: d[k] for k in sort_order if k in d}
        sorted_dict.update({k: v for k, v in d.items() if k not in sorted_dict})
        return sorted_dict

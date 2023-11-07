import re
import os
import lkml
import yaml
import uuid
from collections import defaultdict


class LookMLProject:
    def __init__(self, in_directory: str = None, out_directory: str = None):
        self.in_directory = in_directory
        self.out_directory = out_directory
        self.field_mappings = []
        self._views = []
        self._models = []

    def convert(self):
        if not self.in_directory:
            raise ValueError(
                "You must pass the in_directory argument to the class to use this function. "
                "If you want to convert dict -> dict use the convert_project function in this class"
            )
        lookml_project = self.load(self.in_directory)
        models, views, dashboards = self.convert_project(lookml_project)

        if not self.out_directory:
            raise ValueError(
                "You must pass the out_directory argument to the class to use this function. "
                "If you want to convert dict -> dict use the convert_project function in this class"
            )
        self.dump(self.out_directory, models, views, dashboards)

    def convert_project(self, lookml_project: dict):
        models, views, dashboards = [], [], []
        view_metadata = {}
        views_to_models = {}
        for raw_model in lookml_project["models"]:
            model = self.convert_model(raw_model, generate_view_metadata=True)
            model_view_metadata = model.pop("view_metadata", {})
            view_metadata.update(model_view_metadata)
            for view_name in set(model_view_metadata.keys()):
                views_to_models[view_name] = model["name"]
            models.append(model)
        self._models = models

        default_model_name = models[0]["name"]
        for raw_view in lookml_project["views"]:
            # We don't currently get access filters from the explores
            # because they vary across explores for the same view
            view = self.convert_view(
                raw_view,
                views_to_models.get(raw_view["name"], default_model_name),
                access_filters=[],
                joins=view_metadata.get(raw_view["name"], []),
            )
            views.append(view)
        self._views = views

        for raw_dashboard in lookml_project["dashboards"]:
            dashboard = self.convert_dashboard(raw_dashboard)
            dashboards.append(dashboard)

        return models, views, dashboards

    @staticmethod
    def convert_model(model: dict, generate_view_metadata: bool = False):
        """Convert a LookML model to a ZenML model
        Args: model (dict): A LookML model
              generate_view_metadata (bool): Whether to generate view metadata
                                                based on the explores in the model
        Returns: dict: A ZenML model (if generate_view_metadata is False) or a ZenML
                        with the extra key 'view_metadata' (if generate_view_metadata is True)
        """
        model_yaml = {
            "version": 1,
            "type": "model",
            "name": model["name"],
            "connection": model["connection"],
        }
        if "label" in model:
            model_yaml["label"] = model["label"]
        if "access_grants" in model:
            model_yaml["access_grants"] = model["access_grants"]
        if "week_start_day" in model:
            model_yaml["week_start_day"] = model["week_start_day"].lower()

        if generate_view_metadata:
            model_yaml["view_metadata"] = LookMLProject.get_view_metadata(model)
        return model_yaml

    @staticmethod
    def parse_sql_on(sql_on: str):
        # This code parses a sql_on to determine the relationship between two views
        remaining_sql = sql_on
        references = LookMLProject.fields_to_replace(sql_on)
        for field in references:
            remaining_sql = remaining_sql.replace(f"${{{field}}}", "")

        # Iff this is true then the sql_on is really just comparing two fields to each other
        if remaining_sql.strip() == "=":
            return "identifier", references

        # Otherwise we need to assume the sql_on is custom
        return "custom", references

    def parse_join(join: dict):
        if "sql_on" in join:
            return LookMLProject.parse_sql_on(join["sql_on"])
        else:
            print(f'Skipping join {join} without "sql_on"')

    @staticmethod
    def get_view_metadata(model: dict) -> dict:
        explores = model.get("explores", [])

        identifier_graph = defaultdict(lambda: defaultdict(list))
        for explore in explores:
            root_view = explore["name"] if "from" not in explore else explore["from"]
            for join in explore.get("joins", []):
                pair_id = str(uuid.uuid4())
                join_view = join["name"] if "from" not in join else join["from"]

                # Relationship always corresponds to the root view in the explore
                # many_to_one is the default join type
                relationship = join.get("relationship", "many_to_one")
                join_type, references = LookMLProject.parse_join(join)

                # If the relationship is one_to_one then we can assume that the
                # key's used in the join are unique (primary) in both views
                if relationship == "one_to_one":
                    if join_type == "identifier":
                        for reference in references:
                            view_name, field_name = reference.split(".")
                            identifier = LookMLProject._to_identifier(field_name, "primary", pair_id)
                            identifier_graph[view_name][identifier["sql"]].append(identifier)

                # If the relationship is one_to_many then we can assume that the
                # key's used in the join are unique (primary) ONLY if the key references the root view
                elif relationship == "one_to_many":
                    if join_type == "identifier":
                        for reference in references:
                            view_name, field_name = reference.split(".")
                            if view_name == root_view:
                                identifier = LookMLProject._to_identifier(field_name, "primary", pair_id)
                            else:
                                identifier = LookMLProject._to_identifier(field_name, "foreign", pair_id)
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
                            if view_name == join_view:
                                identifier = LookMLProject._to_identifier(field_name, "primary", pair_id)
                            else:
                                identifier = LookMLProject._to_identifier(field_name, "foreign", pair_id)
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
                    views, ids = LookMLProject._get_pair(pair_id, identifier_graph)
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

        return resolved_id_graph

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
    def convert_view(view: dict, model_name: str, access_filters: list = [], joins: list = []):
        zenml_view = {
            "version": 1,
            "type": "view",
            "name": view["name"],
            "model_name": model_name,
            "required_access_grants": view.get("required_access_grants", []),
            "row_label": view["name"].replace("_", " ").title(),
            "sets": view.get("sets", []),
            "access_filters": access_filters,
            "identifiers": joins,
        }
        dimensions = [
            f for field in view.get("dimensions", []) if (f := LookMLProject.convert_dimension(field))
        ]
        dimension_groups = [
            f
            for field in view.get("dimension_groups", [])
            if (f := LookMLProject.convert_dimension_group(field))
        ]
        measures = [f for field in view.get("measures", []) if (f := LookMLProject.convert_measure(field))]
        zenml_view["fields"] = dimensions + dimension_groups + measures

        if "view_label" in view:
            zenml_view["label"] = view["view_label"]

        if "description" in view:
            zenml_view["description"] = view["description"]

        if "sql_table_name" in view:
            zenml_view["sql_table_name"] = view["sql_table_name"]

        if "derived_table" in view:
            zenml_view["derived_table"]["sql"] = view["derived_table"]["sql"]

        first_date_field = next(
            (f["name"] for f in zenml_view["fields"] if f["field_type"] == "dimension_group"), None
        )
        if first_date_field:
            zenml_view["default_date"] = first_date_field

        return zenml_view

    def convert_dashboard(self, dashboard: dict):
        zenml_data = {
            "version": 1,
            "type": "dashboard",
            "name": dashboard["dashboard"],
            "label": dashboard["title"],
            "elements": [],
        }
        if "description" in dashboard:
            zenml_data["description"] = dashboard["description"]

        for element in dashboard["elements"]:
            zenml_element = self._translate_dashboard_element(element)
            if zenml_element:
                zenml_data["elements"].append(zenml_element)

        return zenml_data

    def _translate_dashboard_element(self, element: dict):
        if "merged_queries" in element:
            return self._translate_merged_queries_element(element)
        return self._translate_vanilla_element(element)

    def _translate_vanilla_element(self, element: dict):
        # We do not support conditional formatting in dashboards
        # We do not support non-query elements yet, either
        if "model" not in element:
            return None

        zenml_element = {"model": element["model"], "metrics": [], "slice_by": []}
        if "title" in element:
            zenml_element["title"] = element["title"]

        # Add fields
        for f in element["fields"]:
            field = self._get_field(f, self._views)
            if field["field_type"] == "measure":
                zenml_element["metrics"].append(f)
            else:
                zenml_element["slice_by"].append(f)

        if "pivots" in element:
            zenml_element["pivot_by"] = element["pivots"]

        if "filters" in element:
            zenml_element["filters"] = []
            for k, v in element["filters"].items():
                zenml_element["filters"].append({"field": k.lower(), "value": v})

        if "sorts" in element:
            zenml_element["sort"] = []
            for sort_str in element["sorts"]:
                split_str = sort_str.split(" ")
                if len(split_str) == 1:
                    zenml_element["sort"].append({"field": split_str[0].lower(), "value": "asc"})
                else:
                    zenml_element["sort"].append(
                        {"field": split_str[0].lower(), "value": split_str[1].lower()}
                    )

        if "show_totals" in element:
            zenml_element["show_totals"] = bool(element["show_totals"])

        if "show_value_labels" in element:
            zenml_element["show_annotations"] = bool(element["show_value_labels"])

        if "limit" in element:
            zenml_element["row_limit"] = element["limit"]

        if "dynamic_fields" in element:
            zenml_element["table_calculations"] = []
            for dynamic_field in element["dynamic_fields"]:
                zenml_element["table_calculations"].append(
                    {
                        "title": dynamic_field["label"],
                        "formula": self._clean_table_calc(dynamic_field["expression"]),
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

        if element.get("type") == "looker_column":
            plot = "grouped_bar" if len(zenml_element["slice_by"]) > 1 else "bar"
            zenml_element["plot_type"] = plot
        elif element.get("type") == "looker_line":
            "line" or "multi_line"
            plot = "multi_line" if len(zenml_element["slice_by"]) > 1 else "line"
            zenml_element["plot_type"] = plot
        elif element.get("type") in plot_lookup:
            zenml_element["plot_type"] = plot_lookup[element["type"]]
            if zenml_element["plot_type"] == "table_only":
                zenml_element["force_table"] = True

        return zenml_element

    def _get_field(self, field_id: str, views: list):
        for v in views:
            for f in v["fields"]:
                if f"{v['name']}.{f['name']}" == field_id.lower() and f["field_type"] != "dimension_group":
                    return f
                elif f"{v['name']}.{f['name']}" in field_id.lower() and f["field_type"] == "dimension_group":
                    return f
        # If we can't find the field assume it will be a dimension on a dashboard
        return {"field_type": "dimension"}

    def _clean_table_calc(self, formula: str):
        for field_to_replace in self.fields_to_replace(formula):
            formula = formula.replace(f"${{{field_to_replace}}}", f"[{field_to_replace}]")
        return formula

    def _translate_merged_queries_element(self, element: dict):
        # We do not support translation for looker filter expressions

        filters_by_expression = defaultdict(list)
        for merged in element["merged_queries"]:
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
        for merged in element["merged_queries"]:
            for f in merged["fields"]:
                # Add fields that are not mappings
                matched_pair = next((pair for pair in self.field_mappings if f in pair), None)

                # We can add one and only one field from the mappings to the running fields
                if matched_pair and all(p not in running_fields for p in matched_pair):
                    running_fields.append(f)

                # We can always add fields that are not in the mappings at all
                if all(f not in pair for pair in self.field_mappings):
                    running_fields.append(f)

        first_element = element["merged_queries"][0]
        first_element["fields"] = running_fields

        return self._translate_vanilla_element(first_element)

    @staticmethod
    def fields_to_replace(text: str):
        if text is None:
            return []
        matches = re.finditer(r"\$\{(.*?)\}", text, re.MULTILINE)
        return [match.group(1) for match in matches]

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
                        lookml_dict = yaml.safe_load(f)
                    lookml["dashboards"].extend(lookml_dict)
        return lookml

    @staticmethod
    def dump(out_directory: str, models: list, views: list, dashboards: list):
        zenlytic_project = {
            "name": "new_zenlytic_project",
            "profile": "new_zenlytic_project",
            "dashboard-paths": ["dashboards"],
            "view-paths": ["views"],
            "model-paths": ["models"],
        }
        with open(os.path.join(out_directory, "zenlytic_project.yml"), "w") as f:
            yaml.dump(zenlytic_project, f)

        for directory in ["models", "views", "dashboards"]:
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

    @staticmethod
    def convert_dimension(dimension_dict: dict):
        converted = {**dimension_dict, "field_type": "dimension"}
        if "hidden" in converted:
            converted["hidden"] = converted["hidden"] == "yes"
        if "primary_key" in converted:
            converted["primary_key"] = converted["primary_key"] == "yes"
        if "tiers" in converted:
            converted["tiers"] = [int(tier) for tier in converted["tiers"]]
        if "type" not in converted:
            converted["type"] = "string"
        if "links" in converted:
            links = converted.pop("links")
            converted["link"] = links[0].get("url")
        return converted

    @staticmethod
    def convert_dimension_group(dimension_group_dict: dict):
        converted = {**dimension_group_dict, "field_type": "dimension_group"}
        if "hidden" in converted:
            converted["hidden"] = converted["hidden"] == "yes"
        if "primary_key" in converted:
            converted["primary_key"] = converted["primary_key"] == "yes"
        if "convert_tz" in converted:
            converted["convert_tz"] = converted["convert_tz"] == "yes"
        if "convert_timezone" in converted:
            converted["convert_timezone"] = converted["convert_timezone"] == "yes"
        return converted

    @staticmethod
    def convert_measure(measure_dict: dict):
        converted = {**measure_dict, "field_type": "measure"}
        # These are types we do not support, so therefore cannot add to the YAML
        if "type" in converted and converted["type"] in {"date", "date_time"}:
            return {}
        if "hidden" in converted:
            converted["hidden"] = converted["hidden"] == "yes"
        if "filters__all" in converted:
            filters = converted.pop("filters__all")
            converted["filters"] = []
            for f in filters:
                if isinstance(f, list):
                    for sub_filter in f:
                        for field, value in sub_filter.items():
                            converted["filters"].append({"field": field.lower(), "value": value})
                else:
                    converted["filters"].append({"field": f["field"].lower(), "value": f["value"]})
        return converted

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

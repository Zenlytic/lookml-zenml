import re
import os
import lkml
import yaml
from collections import defaultdict

# write code to walk through a directory and read lookml files using the lkml package imported above
# and then print the YAML for each model and view in the directory
# hint: use the lkml.load function to read the lookml files


# Path: lookml_zenml/walk.py


class LookMLProject:
    def __init__(self, directory):
        self.directory = directory
        self.field_mappings = []

    def translate(self):
        lookml = self.load()
        models = self.translate_models(lookml)
        views = self.translate_views(lookml)
        dashboards = self.translate_dashboards(lookml)

        # Dump the files and sort
        print(models)
        print(views)
        print(dashboards)

    @staticmethod
    def translate_models(lookml: dict):
        model_yaml_dicts = []
        for model in lookml["models"]:
            model_yaml = LookMLProject.convert_model(model)
            model_yaml_dicts.append(model_yaml)
        return model_yaml_dicts

    def translate_views(self, lookml: dict):
        metadata = self.view_metadata(lookml)
        views = []
        for view in lookml["views"]:
            views.append(self.convert_view(view, metadata))
        return views

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
        elif "foreign_key" in join:
            return "foreign_key", [join["foreign_key"]]
        else:
            print(f'Skipping join {join} without "sql_on" or "foreign_key"')

    @staticmethod
    def get_view_metadata(model: dict):
        explores = model.get("explores", [])
        print(LookMLProject.parse_sql_on("${zendesk_tickets.requester_id}=  ${zendesk_users.user_id}"))

        identifier_graph = defaultdict(list)
        for explore in explores:
            root_view = explore["name"] if "from" not in explore else explore["from"]
            print(root_view)
            for join in explore.get("joins", []):
                join_view = join["name"] if "from" not in join else join["from"]
                print(join_view)
                # Relationship always corresponds to the root view in the explore
                # many_to_one is the default join type
                relationship = join.get("relationship", "many_to_one")
                join_type, references = LookMLProject.parse_join(join)
                print(relationship)
                print(join_type, references)
                # If the relationship is one_to_one then we can assume that the
                # key's used in the join are unique (primary) in both views
                if relationship == "one_to_one":
                    if join_type == "identifier":
                        for reference in references:
                            print(reference)
                            view_name, field_name = reference.split(".")
                            identifier = LookMLProject._to_identifier(field_name, "primary")
                            identifier_graph[view_name].append(identifier)

                elif relationship == "one_to_many":
                    if join_type == "identifier":
                        for reference in references:
                            print(reference)
                            view_name, field_name = reference.split(".")
                            if view_name == root_view:
                                identifier = LookMLProject._to_identifier(field_name, "primary")
                            else:
                                identifier = LookMLProject._to_identifier(field_name, "foreign")
                            identifier_graph[view_name].append(identifier)

                # We do not want to replicate many_to_many joins since they get out of hand quickly
                elif relationship == "many_to_many":
                    pass

                elif relationship == "many_to_one":
                    if join_type == "identifier":
                        for reference in references:
                            print(reference)
                            view_name, field_name = reference.split(".")
                            if view_name == root_view:
                                identifier = LookMLProject._to_identifier(field_name, "foreign")
                            else:
                                identifier = LookMLProject._to_identifier(field_name, "primary")
                            identifier_graph[view_name].append(identifier)
                else:
                    raise NotImplementedError(f"Relationship {relationship} is not supported")

        print(identifier_graph)
        [
            {
                "label": "Signed in Users",
                "joins": [
                    {
                        "view_label": "Profile Facts",
                        "type": "left_outer",
                        "relationship": "one_to_one",
                        "sql_on": "${user_view.id} = ${profile_facts_view.profile_id}",
                        "name": "profile_facts_view",
                    },
                    {
                        "view_label": "Orders",
                        "type": "left_outer",
                        "relationship": "one_to_many",
                        "sql_on": "${user_view.id} = ${orders_view.profile_id}",
                        "name": "orders_view",
                    },
                    {
                        "view_label": "Last Touch Attribution",
                        "type": "left_outer",
                        "relationship": "one_to_many",
                        "sql_on": "${last_touch_attribution_view.profile_id} = ${orders_view.profile_id}",
                        "name": "last_touch_attribution_view",
                    },
                    {
                        "view_label": "Marketing Spend (Aligned on OrderWeek)",
                        "type": "left_outer",
                        "relationship": "one_to_many",
                        "sql_on": "${marketing_spend_daily.date_date} = ${orders_view.orderdatetime_date}",
                        "name": "marketing_spend_daily",
                    },
                ],
                "name": "user_view",
            },
            {
                "from": "all_visitors",
                "label": "Sessions",
                "view_label": "All Visitors",
                "joins": [
                    {
                        "view_label": "Orders",
                        "type": "left_outer",
                        "sql_on": "${user_view.id} = ${orders_view.profile_id}",
                        "relationship": "one_to_many",
                        "name": "orders_view",
                    },
                    {
                        "view_label": "Session to Profile",
                        "from": "session_to_profile",
                        "type": "left_outer",
                        "sql_on": "${all_visitors_view.session_id} = ${session_to_profile_view.session}",
                        "relationship": "one_to_one",
                        "name": "session_to_profile_view",
                    },
                    {
                        "view_label": "User",
                        "type": "left_outer",
                        "sql_on": "${session_to_profile_view.user_id} = ${user_view.id}",
                        "relationship": "many_to_one",
                        "name": "user_view",
                    },
                    {
                        "view_label": "Profile Facts",
                        "type": "left_outer",
                        "relationship": "one_to_one",
                        "sql_on": "${user_view.id} = ${profile_facts_view.profile_id}",
                        "name": "profile_facts_view",
                    },
                ],
                "name": "all_visitors_view",
            },
            {
                "label": "Zendesk",
                "joins": [
                    {
                        "view_label": "User",
                        "type": "left_outer",
                        "sql_on": "${zendesk_users.email} =${user_view.email}",
                        "relationship": "one_to_one",
                        "name": "user_view",
                    },
                    {
                        "view_label": "Orders",
                        "type": "left_outer",
                        "sql_on": "${user_view.id} = ${orders_view.profile_id}",
                        "relationship": "one_to_many",
                        "fields": [
                            "orders_view.id",
                            "orders_view.profile_id",
                            "orders_view.orderdatetime_date",
                            "orders_view.orderdatetime_raw",
                            "orders_view.orderdatetime_week",
                            "orders_view.orderdatetime_month",
                            "orders_view.order_count",
                            "orders_view.first_order",
                            "orders_view.latest_order",
                        ],
                        "name": "orders_view",
                    },
                    {
                        "type": "left_outer",
                        "relationship": "one_to_one",
                        "sql_on": "${zendesk_tickets.requester_id}=  ${zendesk_users.user_id}",
                        "name": "zendesk_users",
                    },
                ],
                "name": "zendesk_tickets",
            },
        ]
        raise NotImplementedError()

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

    def translate_dashboards(self, lookml: dict):
        return [self._translate_dashboard(dashboard) for dashboard in lookml["dashboards"]]

    def _translate_dashboard(self, dashboard: dict):
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
            zenml_data["elements"].append(zenml_element)

        return zenml_data

    def _translate_dashboard_element(self, element: dict):
        if "merged_queries" in element:
            return self._translate_merged_queries_element(element)
        return self._translate_vanilla_element(element)

    def _translate_vanilla_element(self, element: dict):
        # We do not support conditional formatting in dashboards
        zenml_element = {"title": element["title"], "model": element["model"], "metrics": [], "slice_by": []}

        # Add fields
        for f in element["fields"]:
            field = self.zenlytic_project.get_field(f)
            if field.field_type == "measure":
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
                    zenml_element["sorts"].append({"field": split_str[0].lower(), "value": "asc"})
                else:
                    zenml_element["sorts"].append(
                        {"field": split_str[0].lower(), "value": split_str[1].lower()}
                    )
                zenml_element["filters"].append({"field": k, "value": v})

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
            "bar" or "grouped_bar"
            zenml_element["plot_type"] = "plot"
        elif element.get("type") == "looker_line":
            "line" or "multi_line"
            zenml_element["plot_type"] = "plot"
        elif element.get("type") in plot_lookup:
            zenml_element["plot_type"] = plot_lookup[element["type"]]
            if zenml_element["plot_type"] == "table_only":
                zenml_element["force_table"] = True

        return zenml_element

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

    def fields_to_replace(text: str):
        matches = re.finditer(r"\$\{(.*?)\}", text, re.MULTILINE)
        return [match.group(1) for match in matches]

    def load(self):
        lookml = {"views": [], "models": [], "dashboards": []}
        for root, _, files in os.walk(self.directory):
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
    def _to_identifier(field_name: str, type: str):
        return {"name": field_name, "type": type, "sql": f"${{{field_name}}}"}

    @staticmethod
    def is_lookml_file(file):
        suffixes = [".model.lkml", ".view.lkml", ".model.lookml", ".view.lookml"]
        return any(file.endswith(suffix) for suffix in suffixes)

    @staticmethod
    def is_lookml_dashboard_file(file):
        suffixes = [".dashboard.lkml", ".dashboard.lookml"]
        return any(file.endswith(suffix) for suffix in suffixes)

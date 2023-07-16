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
                model_yaml["week_start_day"] = model["week_start_day"]

            model_yaml_dicts.append(model_yaml)
        return model_yaml_dicts

    def translate_views(self, lookml: dict):
        metadata = self.view_metadata(lookml)
        views = []
        for view in lookml["views"]:
            views.append(self._translate_view(view, metadata))
        return views

    def view_metadata(lookml: dict):
        raise NotImplementedError()
        return {}

    def _translate_view(view: dict, view_metadata: dict):
        zenml_view = {
            "version": 1,
            "type": "view",
            "name": view["name"],
            "label": view.get("view_label"),
            "description": view.get("description"),
            "model_name": view_metadata[view["name"]]["model_name"],
            "required_access_grants": view.get("required_access_grants", []),
            "row_label": view["name"].replace("_", " ").title(),
            "sets": view.get("sets", []),
            "access_filter": view_metadata[view["name"]].get("access_filters", []),
            "identifiers": view_metadata[view["name"]].get("joins", []),
            "fields": [
                {
                    "name": field["name"],
                    "label": field.get("label"),
                    "view_label": field.get("view_label"),
                    "group_label": field.get("group_label"),
                    "value_format_name": field.get("value_format_name"),
                    "field_type": field.get("type", "dimension"),
                    "type": field.get("type"),
                    "sql": field.get("sql"),
                    "tags": field.get("tags"),
                    "drill_fields": field.get("drill_fields"),
                    "primary_key": field.get("primary_key") != "no",
                    "hidden": field.get("hidden") == "no",
                    "case": field.get("case"),
                    "tiers": field.get("tiers"),
                    "required_access_grants": field.get("required_access_grants"),
                    "link": field.get("links")[0].get("url") if field.get("links") else None,
                    "timeframes": field.get("timeframes"),
                    "convert_tz": field.get("convert_tz") != "no",
                    "datatype": field.get("datatype"),
                    "intervals": field.get("intervals"),
                    "sql_start": field.get("sql_start"),
                    "sql_end": field.get("sql_end"),
                    "sql_distinct_key": field.get("sql_distinct_key"),
                    "filters": field.get("filters__all"),
                }
                for field in view["dimensions"]
            ],
        }

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
    def is_lookml_file(file):
        suffixes = [".model.lkml", ".view.lkml", ".model.lookml", ".view.lookml"]
        return any(file.endswith(suffix) for suffix in suffixes)

    @staticmethod
    def is_lookml_dashboard_file(file):
        suffixes = [".dashboard.lkml", ".dashboard.lookml"]
        return any(file.endswith(suffix) for suffix in suffixes)

import re
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union, Any, Literal


def fields_to_replace(text: str) -> List[str]:
    if text is None:
        return []
    matches = re.finditer(r"\$\{(.*?)\}", text, re.MULTILINE)
    return [match.group(1) for match in matches]


# Pydantic models for LookML structures
class LookMLDerivedTable(BaseModel):
    """Pydantic model for LookML derived table."""

    sql: str
    sql_trigger_value: Optional[str] = None
    datagroup_trigger: Optional[str] = None
    persist_for: Optional[str] = None
    indexes: Optional[List[str]] = None
    distribution_style: Optional[str] = None
    sortkeys: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLDerivedTable":
        """Create LookMLDerivedTable from dictionary."""
        data = data.copy()
        if "explore_source" in data:
            raise NotImplementedError(
                f"explore_source is not implemented as a valid view data source. "
                f"Please remove the file and try conversion again. data: {data}"
            )
        return cls(**data)


class LookMLLink(BaseModel):
    """Pydantic model for LookML link."""

    url: str
    name: Optional[str] = None


class LookMLDimension(BaseModel):
    """Pydantic model for LookML dimension."""

    name: str
    type: Optional[str] = "string"
    sql: Optional[str] = None
    description: Optional[str] = None
    label: Optional[str] = None
    view_label: Optional[str] = None
    group_label: Optional[str] = None
    value_format: Optional[str] = None
    value_format_name: Optional[str] = None
    primary_key: Optional[str] = None
    hidden: Optional[str] = None
    drill_fields: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    required_access_grants: Optional[List[str]] = None
    links: Optional[List[LookMLLink]] = None
    tiers: Optional[List[int]] = None
    case: Optional[Dict[str, Any]] = None
    alpha_sort: Optional[bool] = None
    order_by_field: Optional[str] = None
    suggest_dimension: Optional[str] = None
    suggest_explore: Optional[str] = None
    suggestions: Optional[List[str]] = None
    bypass_suggest_restrictions: Optional[bool] = None
    full_suggestions: Optional[bool] = None
    can_filter: Optional[bool] = None
    fanout_on: Optional[str] = None
    sql_latitude: Optional[str] = None
    sql_longitude: Optional[str] = None
    map_layer_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLDimension":
        """Create LookMLDimension from dictionary."""
        # Parse links if present
        if "links" in data and data["links"]:
            parsed_links = []
            for link in data["links"]:
                if isinstance(link, dict):
                    parsed_links.append(LookMLLink.from_dict(link))
                else:
                    parsed_links.append(LookMLLink(url=link))
            data["links"] = parsed_links

        return cls(**data)


class LookMLDimensionGroup(BaseModel):
    """Pydantic model for LookML dimension group."""

    name: str
    type: Literal["time", "date", "datetime", "duration"] = "time"
    primary_key: Optional[str] = None
    sql: Optional[str] = None
    description: Optional[str] = None
    label: Optional[str] = None
    view_label: Optional[str] = None
    group_label: Optional[str] = None
    timeframes: Optional[List[str]] = None
    intervals: Optional[List[str]] = None
    convert_tz: Optional[str] = None
    convert_timezone: Optional[str] = None
    datatype: Optional[str] = None
    sql_start: Optional[str] = None
    sql_end: Optional[str] = None
    hidden: Optional[bool] = None
    drill_fields: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    required_access_grants: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLDimensionGroup":
        """Create LookMLDimensionGroup from dictionary."""
        return cls(**data)


class LookMLFilter(BaseModel):
    """Pydantic model for LookML filter."""

    field: str
    value: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLFilter":
        """Create LookMLFilter from dictionary."""
        return cls(**data)

    @classmethod
    def process_list_of_filters(
        cls, filters: List[Dict[str, Any]], alias_to_view_mapping: Dict[str, str] = {}
    ) -> List["LookMLFilter"]:
        """Process a list of filters and return a list of LookMLFilter objects."""

        filter_objects = []
        for f in filters:
            if isinstance(f, list):
                for sub_filter in f:
                    for field, value in sub_filter.items():
                        field = LookMLFilter.replace_field_alias_with_view(field, alias_to_view_mapping)
                        filter_objects.append(cls(field=field.lower(), value=value))
            else:
                field = LookMLFilter.replace_field_alias_with_view(f["field"], alias_to_view_mapping)
                filter_objects.append(cls(field=field.lower(), value=f["value"]))

        return filter_objects

    @staticmethod
    def replace_field_alias_with_view(field_id: str, alias_to_view_mapping: Dict[str, str]) -> str:
        """Replace a field alias with the corresponding view name."""
        if "." in field_id:
            view_name = field_id.split(".")[0]
            field_name = field_id.split(".")[1]
            if view_name in alias_to_view_mapping:
                view_name = alias_to_view_mapping[view_name]
                field_id = view_name + "." + field_name
        return field_id


class LookMLMeasure(BaseModel):
    """Pydantic model for LookML measure."""

    name: str
    type: str = "count"
    sql: Optional[str] = None
    description: Optional[str] = None
    label: Optional[str] = None
    view_label: Optional[str] = None
    group_label: Optional[str] = None
    value_format: Optional[str] = None
    value_format_name: Optional[str] = None
    hidden: Optional[str] = None
    drill_fields: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    required_access_grants: Optional[List[str]] = None
    filters: Optional[List[LookMLFilter]] = None
    sql_distinct_key: Optional[str] = None
    percentile: Optional[int] = None
    approximate: Optional[bool] = None
    approximate_threshold: Optional[int] = None
    direction: Optional[str] = None
    can_filter: Optional[bool] = None
    link: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLMeasure":
        """Create LookMLMeasure from dictionary with nested filter conversion."""
        # Convert nested filters
        if "filters__all" in data and data["filters__all"]:
            data = data.copy()
            filters = data.pop("filters__all")
            data["filters"] = LookMLFilter.process_list_of_filters(filters)

        return cls(**data)


class LookMLSet(BaseModel):
    """Pydantic model for LookML set."""

    name: str
    fields: List[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLSet":
        """Create LookMLSet from dictionary."""
        return cls(**data)


class LookMLAccessFilter(BaseModel):
    """Pydantic model for LookML access filter."""

    field: str
    user_attribute: str

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], alias_to_view_mapping: Dict[str, str] = {}
    ) -> "LookMLAccessFilter":
        """Create LookMLAccessFilter from dictionary."""
        data = data.copy()
        if "field" in data:
            data["field"] = LookMLFilter.replace_field_alias_with_view(data["field"], alias_to_view_mapping)
        return cls(**data)


class LookMLView(BaseModel):
    """Pydantic model for LookML view."""

    name: str
    extends: Optional[List[str]] = []
    extension: Optional[str] = None
    view_label: Optional[str] = None
    description: Optional[str] = None
    fields_hidden_by_default: Optional[str] = None
    sql_table_name: Optional[str] = None
    derived_table: Optional[LookMLDerivedTable] = None
    required_access_grants: Optional[List[str]] = []
    sets: Optional[List[LookMLSet]] = []
    dimensions: Optional[List[LookMLDimension]] = []
    dimension_groups: Optional[List[LookMLDimensionGroup]] = []
    measures: Optional[List[LookMLMeasure]] = []
    filters: Optional[List[Dict[str, Any]]] = []
    parameters: Optional[List[Dict[str, Any]]] = []

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLView":
        """Create LookMLView from dictionary with nested type conversion."""
        data = data.copy()

        if "extends__all" in data:
            data["extends"] = [extends for collection in data["extends__all"] for extends in collection]

        # Convert nested derived_table
        if "derived_table" in data and data["derived_table"]:
            try:
                data["derived_table"] = LookMLDerivedTable.from_dict(data["derived_table"])
            except NotImplementedError as e:
                raise NotImplementedError(f"In the view {data['name']}, {str(e)}")

        # Convert nested sets
        if "sets" in data and data["sets"]:
            data["sets"] = [LookMLSet.from_dict(s) if isinstance(s, dict) else s for s in data["sets"]]

        # Convert nested dimensions
        if "dimensions" in data and data["dimensions"]:
            data["dimensions"] = [
                LookMLDimension.from_dict(d) if isinstance(d, dict) else d for d in data["dimensions"]
            ]

        # Convert nested dimension_groups
        if "dimension_groups" in data and data["dimension_groups"]:
            data["dimension_groups"] = [
                LookMLDimensionGroup.from_dict(dg) if isinstance(dg, dict) else dg
                for dg in data["dimension_groups"]
            ]

        # Convert nested measures
        if "measures" in data and data["measures"]:
            data["measures"] = [
                LookMLMeasure.from_dict(m) if isinstance(m, dict) else m for m in data["measures"]
            ]

        return cls(**data)


class LookMLJoin(BaseModel):
    """Pydantic model for LookML join."""

    name: str
    type: Optional[str] = "left_outer"
    relationship: Optional[str] = "many_to_one"
    sql_on: Optional[str] = None
    from_: Optional[str] = Field(None, alias="from")
    view_label: Optional[str] = None
    fields: Optional[List[str]] = None
    required_joins: Optional[List[str]] = None
    foreign_key: Optional[str] = None
    sql_table_name: Optional[str] = None
    sql_where: Optional[str] = None
    required_access_grants: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any], alias_to_view_mapping: Dict[str, str] = {}) -> "LookMLJoin":
        """Create LookMLJoin from dictionary."""
        data = data.copy()
        if "from" in data and data["from"] != data["name"]:
            alias_to_view_mapping[data["name"]] = data["from"]
        if "sql_on" in data:
            for f in fields_to_replace(data["sql_on"]):
                new_field = LookMLFilter.replace_field_alias_with_view(f, alias_to_view_mapping)
                data["sql_on"] = data["sql_on"].replace("${" + f + "}", "${" + new_field + "}")
        if "sql_where" in data:
            for f in fields_to_replace(data["sql_where"]):
                new_field = LookMLFilter.replace_field_alias_with_view(f, alias_to_view_mapping)
                data["sql_where"] = data["sql_where"].replace("${" + f + "}", "${" + new_field + "}")
        if "sql_where" in data and "sql_on" in data:
            data["sql_on"] = data["sql_on"] + " AND " + data["sql_where"]
        return cls(**data)


class LookMLAlwaysFilter(BaseModel):
    """Pydantic model for LookML always filter."""

    filters: List[LookMLFilter]

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], alias_to_view_mapping: Dict[str, str] = {}
    ) -> "LookMLAlwaysFilter":
        """Create LookMLAlwaysFilter from dictionary with nested filter conversion."""
        data = data.copy()

        # Convert nested filters
        if "filters__all" in data and data["filters__all"]:
            filters = data.pop("filters__all")
            data["filters"] = LookMLFilter.process_list_of_filters(filters, alias_to_view_mapping)

        return cls(**data)


class LookMLConditionallyFilter(BaseModel):
    """Pydantic model for LookML conditionally filter."""

    filters: List[LookMLFilter]
    unless: Optional[List[str]] = None

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], alias_to_view_mapping: Dict[str, str] = {}
    ) -> "LookMLConditionallyFilter":
        """Create LookMLConditionallyFilter from dictionary with nested filter conversion."""
        data = data.copy()

        if "filters__all" in data and data["filters__all"]:
            filters = data.pop("filters__all")
            data["filters"] = LookMLFilter.process_list_of_filters(filters, alias_to_view_mapping)

        return cls(**data)


class LookMLExploreFrom(BaseModel):
    """Pydantic model for the LookML explore 'from' field.

    This represents the base view that an explore is built from.
    """

    name: str
    view_label: Optional[str] = None
    label: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Union[Dict[str, Any], str]) -> "LookMLExploreFrom":
        """Create LookMLExploreFrom from dictionary."""

        if isinstance(data, dict):
            data = data.copy()
            return cls(**data)
        else:
            return cls(name=data)


class LookMLExplore(BaseModel):
    """Pydantic model for LookML explore."""

    name: str
    description: Optional[str] = None
    label: Optional[str] = None
    group_label: Optional[str] = None
    view_label: Optional[str] = None
    from_: Optional[LookMLExploreFrom] = Field(None, alias="from")
    view_name: Optional[str] = None
    extends: Optional[List[str]] = None
    extension: Optional[str] = None
    hidden: Optional[str] = None
    fields: Optional[List[str]] = None
    sql_always_where: Optional[str] = None
    required_access_grants: Optional[List[str]] = None
    always_filter: Optional[LookMLAlwaysFilter] = None
    conditionally_filter: Optional[LookMLConditionallyFilter] = None
    access_filter: Optional[List[LookMLAccessFilter]] = None
    always_join: Optional[List[str]] = None
    joins: Optional[List[LookMLJoin]] = []
    persist_for: Optional[str] = None
    persist_with: Optional[str] = None
    case_sensitive: Optional[bool] = None
    sql_table_name: Optional[str] = None
    cancel_grouping_fields: Optional[List[str]] = None
    symmetric_aggregates: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLExplore":
        """Create LookMLExplore from dictionary with nested type conversion."""
        data = data.copy()

        alias_to_view_mapping = {}
        if "view_name" in data and "name" in data:
            alias_to_view_mapping[data["name"]] = data["view_name"]

        # Convert nested from field
        if "from" in data and "name" in data:
            data["from"] = LookMLExploreFrom.from_dict(data["from"])
            alias_to_view_mapping[data["name"]] = data["from"].name

        # Convert nested joins
        if "joins" in data and data["joins"]:
            data["joins"] = [
                LookMLJoin.from_dict(j, alias_to_view_mapping) if isinstance(j, dict) else j
                for j in data["joins"]
            ]

        # Convert nested always_filter
        if "always_filter" in data and data["always_filter"]:
            data["always_filter"] = LookMLAlwaysFilter.from_dict(data["always_filter"], alias_to_view_mapping)

        # Convert nested conditionally_filter
        if "conditionally_filter" in data and data["conditionally_filter"]:
            data["conditionally_filter"] = LookMLConditionallyFilter.from_dict(
                data["conditionally_filter"], alias_to_view_mapping
            )

        # Convert nested access_filter
        if "access_filter" in data and data["access_filter"]:
            data["access_filter"] = [
                LookMLAccessFilter.from_dict(af, alias_to_view_mapping) if isinstance(af, dict) else af
                for af in data["access_filter"]
            ]

        return cls(**data)


class LookMLDatagroup(BaseModel):
    """Pydantic model for LookML datagroup."""

    name: str
    sql_trigger: str
    max_cache_age: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLDatagroup":
        """Create LookMLDatagroup from dictionary."""
        return cls(**data)


class LookMLAccessGrant(BaseModel):
    """Pydantic model for LookML access grant."""

    name: str
    user_attribute: str
    allowed_values: List[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLAccessGrant":
        """Create LookMLAccessGrant from dictionary."""
        return cls(**data)


class LookMLNamedValueFormat(BaseModel):
    """Pydantic model for LookML named value format."""

    name: str
    value_format: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLNamedValueFormat":
        """Create LookMLNamedValueFormat from dictionary."""
        return cls(**data)


class LookMLMapLayer(BaseModel):
    """Pydantic model for LookML map layer."""

    name: str
    file: Optional[str] = None
    url: Optional[str] = None
    format: Optional[str] = None
    projection: Optional[str] = None
    extents_json_url: Optional[str] = None
    feature_key: Optional[str] = None
    property_key: Optional[str] = None
    property_label_key: Optional[str] = None
    label: Optional[str] = None
    max_zoom_level: Optional[int] = None
    min_zoom_level: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLMapLayer":
        """Create LookMLMapLayer from dictionary."""
        return cls(**data)


class LookMLTest(BaseModel):
    """Pydantic model for LookML test."""

    name: str
    explore_source: Dict[str, Any]
    assert_: List[Dict[str, Any]] = Field(alias="assert")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLTest":
        """Create LookMLTest from dictionary."""
        return cls(**data)


class LookMLModel(BaseModel):
    """Pydantic model for LookML model."""

    name: str
    connection: str
    label: Optional[str] = None
    include: Optional[List[str]] = None
    fiscal_month_offset: Optional[int] = None
    persist_for: Optional[str] = None
    persist_with: Optional[str] = None
    case_sensitive: Optional[bool] = None
    week_start_day: Optional[str] = None
    datagroups: Optional[List[LookMLDatagroup]] = None
    access_grants: Optional[List[LookMLAccessGrant]] = []
    named_value_formats: Optional[List[LookMLNamedValueFormat]] = []
    map_layers: Optional[List[LookMLMapLayer]] = []
    tests: Optional[List[LookMLTest]] = []
    explores: Optional[List[LookMLExplore]] = []

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLModel":
        """Create LookMLModel from dictionary with nested type conversion."""
        data = data.copy()

        # Convert nested datagroups
        if "datagroups" in data and data["datagroups"]:
            data["datagroups"] = [
                LookMLDatagroup.from_dict(dg) if isinstance(dg, dict) else dg for dg in data["datagroups"]
            ]

        # Convert nested access_grants
        if "access_grants" in data and data["access_grants"]:
            data["access_grants"] = [
                LookMLAccessGrant.from_dict(ag) if isinstance(ag, dict) else ag
                for ag in data["access_grants"]
            ]

        # Convert nested named_value_formats
        if "named_value_formats" in data and data["named_value_formats"]:
            data["named_value_formats"] = [
                LookMLNamedValueFormat.from_dict(nvf) if isinstance(nvf, dict) else nvf
                for nvf in data["named_value_formats"]
            ]

        # Convert nested map_layers
        if "map_layers" in data and data["map_layers"]:
            data["map_layers"] = [
                LookMLMapLayer.from_dict(ml) if isinstance(ml, dict) else ml for ml in data["map_layers"]
            ]

        # Convert nested tests
        if "tests" in data and data["tests"]:
            data["tests"] = [LookMLTest.from_dict(t) if isinstance(t, dict) else t for t in data["tests"]]

        # Convert nested explores
        if "explores" in data and data["explores"]:
            data["explores"] = [
                LookMLExplore.from_dict(e) if isinstance(e, dict) else e for e in data["explores"]
            ]

        return cls(**data)


class LookMLDashboardFilter(BaseModel):
    """Pydantic model for LookML dashboard filter."""

    name: str
    field: str
    default_value: Optional[Union[str, bool, int, float]] = None
    model: Optional[str] = None
    explore: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLDashboardFilter":
        """Create LookMLDashboardFilter from dictionary."""
        return cls(**data)


class LookMLDashboardElement(BaseModel):
    """Pydantic model for LookML dashboard element."""

    name: str
    title: Optional[str] = None
    model: Optional[str] = None
    explore: Optional[str] = None
    type: Optional[str] = None
    fields: Optional[List[str]] = None
    pivots: Optional[List[str]] = None
    filters: Optional[Dict[str, str]] = None
    sorts: Optional[List[str]] = None
    limit: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    row: Optional[int] = 0
    col: Optional[int] = 0
    stacking: Optional[str] = None
    listen: Optional[Dict[str, str]] = None
    show_totals: Optional[bool] = None
    show_value_labels: Optional[bool] = None
    dynamic_fields: Optional[List[Dict[str, Any]]] = None
    merged_queries: Optional[List[Dict[str, Any]]] = None
    body_text: Optional[str] = None
    rich_content_json: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLDashboardElement":
        """Create LookMLDashboardElement from dictionary."""
        return cls(**data)


class LookMLDashboard(BaseModel):
    """Pydantic model for LookML dashboard."""

    dashboard: str
    title: str
    description: Optional[str] = None
    layout: Optional[str] = None
    preferred_viewer: Optional[str] = None
    filters: Optional[List[LookMLDashboardFilter]] = None
    elements: Optional[List[LookMLDashboardElement]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLDashboard":
        """Create LookMLDashboard from dictionary with nested type conversion."""
        data = data.copy()

        # Convert nested filters
        if "filters" in data and data["filters"]:
            data["filters"] = [
                LookMLDashboardFilter.from_dict(f) if isinstance(f, dict) else f for f in data["filters"]
            ]

        # Convert nested elements
        if "elements" in data and data["elements"]:
            data["elements"] = [
                LookMLDashboardElement.from_dict(e) if isinstance(e, dict) else e for e in data["elements"]
            ]

        return cls(**data)


class LookMLProject(BaseModel):
    """Pydantic model for complete LookML project."""

    models: List[LookMLModel]
    views: List[LookMLView]
    dashboards: List[LookMLDashboard]
    explores: Optional[List[LookMLExplore]] = []

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LookMLProject":
        """Create LookMLProject from dictionary with nested type conversion."""
        data = data.copy()

        # Convert nested models
        if "models" in data and data["models"]:
            data["models"] = [LookMLModel.from_dict(m) if isinstance(m, dict) else m for m in data["models"]]

        # Convert nested views
        if "views" in data and data["views"]:
            data["views"] = [LookMLView.from_dict(v) if isinstance(v, dict) else v for v in data["views"]]

        # Convert nested dashboards
        if "dashboards" in data and data["dashboards"]:
            data["dashboards"] = [
                LookMLDashboard.from_dict(d) if isinstance(d, dict) else d for d in data["dashboards"]
            ]

        # Convert nested explores
        if "explores" in data and data["explores"]:
            data["explores"] = [
                LookMLExplore.from_dict(e) if isinstance(e, dict) else e for e in data["explores"]
            ]

        return cls(**data)

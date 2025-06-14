import pytest
from lookml_zenml.lookml_project import LookMLProjectConverter
from lookml_zenml.lookml_models import (
    LookMLDimension,
    LookMLDimensionGroup,
    LookMLMeasure,
)


@pytest.mark.unit
@pytest.mark.parametrize(
    "lkml_dimension",
    [
        {
            "name": "first_or_recurring_legit_order",
            "description": "'First' denotes the first legit order; 'recurring' is for any legit order after the first",  # noqa
            "case": {
                "whens": [
                    {"sql": "${legit_order_sequence} = 1", "label": "First"},
                    {"sql": "${legit_order_sequence} > 1", "label": "Recurring"},
                    {"sql": "${legit_order_sequence} IS NULL", "label": "Not Legit"},
                ],
                "else": "Unknown",
            },
            "hidden": "yes",
        },
        {
            "name": "discount_percent_tier",
            "type": "tier",
            "tiers": ["1", "11", "21", "31", "41", "51"],
            "style": "integer",
            "sql": "${discount_percent_dim}",
            "hidden": "yes",
        },
        {
            "name": "legit_order_sequence",
            "description": "A 'legit' order is one that is not refunded nor is it designated as a 'trial'",
            "type": "number",
            "sql": "${TABLE}.legit_order_sequence",
            "hidden": "no",
        },
        {
            "name": "id",
            "primary_key": "yes",
            "description": "Unique ID for each order instance",
            "type": "number",
            "sql": "${TABLE}.id",
        },
        {
            "name": "carrier",
            "description": "Mail carrier responsible for delivery of package",
            "sql": "${TABLE}.carrier",
            "required_access_grants": ["test_access_grant"],
        },
    ],
)
def test_dimension_conversion(lkml_dimension):
    converted = LookMLProjectConverter.convert_dimension(LookMLDimension.from_dict(lkml_dimension))

    if lkml_dimension["name"] in {"first_or_recurring_legit_order"}:
        correct = {**lkml_dimension, "hidden": True, "type": "string"}
    elif lkml_dimension["name"] == "legit_order_sequence":
        correct = {**lkml_dimension, "hidden": False}
    elif lkml_dimension["name"] == "discount_percent_tier":
        base_values = {k: v for k, v in lkml_dimension.items() if k != "style"}
        correct = {**base_values, "tiers": [1, 11, 21, 31, 41, 51], "hidden": True}
    elif lkml_dimension["name"] == "id":
        correct = {**lkml_dimension, "primary_key": True}
    elif lkml_dimension["name"] == "carrier":
        correct = {**lkml_dimension, "type": "string"}
    correct["field_type"] = "dimension"

    assert converted == correct


@pytest.mark.unit
@pytest.mark.parametrize(
    "lkml_dimension_group",
    [
        {
            "description": "Time that customer placed the order",
            "type": "time",
            "timeframes": [
                "raw",
                "time",
                "date",
                "day_of_week",
                "day_of_week_index",
                "hour_of_day",
                "month_name",
                "hour",
                "week",
                "month",
                "quarter",
                "year",
                "fiscal_month_num",
                "week_of_year",
            ],
            "sql": "${TABLE}.orderdatetime",
            "convert_tz": "yes",
            "name": "orderdatetime",
            "required_access_grants": ["test_access_grant"],
        }
    ],
)
def test_dimension_group_conversion(lkml_dimension_group):
    converted = LookMLProjectConverter.convert_dimension_group(
        LookMLDimensionGroup.from_dict(lkml_dimension_group)
    )

    if lkml_dimension_group["name"] == "orderdatetime":
        correct = {**lkml_dimension_group, "convert_tz": True}
    correct["field_type"] = "dimension_group"

    assert converted == correct


@pytest.mark.unit
@pytest.mark.parametrize(
    "lkml_measure",
    [
        {
            "label": "First Order Date",
            "type": "date",
            "sql": "MIN(${orderdatetime_raw})",
            "convert_tz": "no",
            "hidden": "yes",
            "name": "first_order",
        },
        {
            "label": "Latest Order Date",
            "type": "date_time",
            "sql": "MAX(${orderdatetime_raw})",
            "convert_tz": "no",
            "hidden": "no",
            "name": "latest_order",
        },
        {
            "type": "sum_distinct",
            "sql_distinct_key": "${order_id}",
            "description": "Net Revenue in USD dollars; includes lead_sku and addons",
            "sql": "((${net_revenue_lead_sku}+ ${add_on_revenue})*1.00)/100",
            "value_format_name": "usd",
            "hidden": "yes",
            "name": "net_revenue_including_addons",
        },
        {
            "type": "number",
            "sql": "(${total_gross_revenue} - ${total_net_revenue}) / ${total_gross_revenue}",
            "value_format_name": "percent_2",
            "hidden": "yes",
            "name": "discount_percent",
            "required_access_grants": ["test_access_grant"],
        },
        {
            "label": "Distinct Purchasers",
            "type": "count_distinct",
            "sql": "${profile_id}",
            "description": "How many distinct purchasers we have. Based on distinct profile_ids",
            "name": "distinct_purchasers",
        },
        {
            "label": "Distinct Blog Purchasers",
            "type": "count_distinct",
            "sql": "${profile_id}",
            "description": "How many distinct purchasers we have. Based on distinct profile_ids",
            "filters__all": [{"field": "permanent_session_view.entry_page", "value": "-%blog%"}],
            "name": "distinct_blog_purchasers",
        },
        {
            "label": "Distinct Blog Purchasers",
            "type": "count_distinct",
            "sql": "${profile_id}",
            "description": "How many distinct purchasers we have. Based on distinct profile_ids",
            "filters__all": [
                {"field": "permanent_session_view.entry_page", "value": "-%blog%"},
                [{"permanent_session_view.referrer": "influencer"}],
            ],
            "name": "distinct_influencer_blog_purchasers",
        },
    ],
)
def test_measure_conversion(lkml_measure):
    converted = LookMLProjectConverter.convert_measure(LookMLMeasure.from_dict(lkml_measure))

    if lkml_measure["name"] in {"latest_order", "first_order"}:
        correct = {}
    elif lkml_measure["name"] in {"net_revenue_including_addons", "discount_percent"}:
        correct = {**lkml_measure, "hidden": True}
        correct["field_type"] = "measure"
    elif lkml_measure["name"] == "distinct_purchasers":
        correct = {**lkml_measure}
        correct["field_type"] = "measure"
    elif lkml_measure["name"] == "distinct_blog_purchasers":
        correct = {**lkml_measure}
        filters = correct.pop("filters__all")
        correct["filters"] = filters
        correct["field_type"] = "measure"
    elif lkml_measure["name"] == "distinct_influencer_blog_purchasers":
        correct = {**lkml_measure}
        correct.pop("filters__all")
        correct["filters"] = [
            {"field": "permanent_session_view.entry_page", "value": "-%blog%"},
            {"field": "permanent_session_view.referrer", "value": "influencer"},
        ]
        correct["field_type"] = "measure"

    assert converted == correct


# @pytest.mark.unit
# @pytest.mark.parametrize(
#     "mf_entity",
#     [
#         {"name": "transaction", "type": "primary", "expr": "id_transaction"},
#         {"name": "order", "type": "foreign", "expr": "id_order"},
#         {"name": "order_line", "type": "unique", "expr": "CAST(id_order_line AS STRING)"},
#     ],
# )
# def test_entity_conversion(mf_entity):
#     converted = convert_mf_entity_to_zenlytic_identifier(mf_entity)

#     if mf_entity["name"] == "transaction":
#         correct = {"name": "transaction", "type": "primary", "sql": "${id_transaction}"}
#     elif mf_entity["name"] == "order":
#         correct = {"name": "order", "type": "foreign", "sql": "${id_order}"}
#     elif mf_entity["name"] == "order_line":
#         correct = {"name": "order_line", "type": "primary", "sql": "CAST(id_order_line AS STRING)"}

#     assert converted == correct

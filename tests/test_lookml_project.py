import pytest
from .conftest import ALL_FIELDS_DIRECTORY, DATA_MODEL_DIRECTORY
from lookml_zenml.lookml_project import LookMLProjectConverter


@pytest.mark.unit
def test_lookml_project_load():
    project = LookMLProjectConverter()
    project_dict = project.load(in_directory=ALL_FIELDS_DIRECTORY)

    assert project_dict["models"][0]["name"] == "model_with_all_fields"
    assert project_dict["models"][0]["connection"] == "connection_name"
    assert project_dict["views"][0]["name"] == "view_name"
    assert project_dict["dashboards"][0]["title"] == "Funnel Conversion Data"


@pytest.mark.unit
def test_lookml_project_convert_project():
    project = LookMLProjectConverter()
    project_dict = project.load(in_directory=DATA_MODEL_DIRECTORY)

    models, views, dashboards, topics = project.convert_project(project_dict)
    refinement_view = next(v for v in views if v["name"] == "churn")

    # Test the refinement wasn't added separately
    assert len([v for v in views if "churn" in v["name"]]) == 1
    assert refinement_view["sql_table_name"] == "`prod.churn_details`"
    assert any(f["name"] == "total_churns" for f in refinement_view["fields"])
    assert any(f["name"] == "churn" for f in refinement_view["fields"])
    assert any(f["name"] == "account_id" for f in refinement_view["fields"])

    ext_base_view = next(v for v in views if v["name"] == "support_interactions")

    assert ext_base_view["model_name"] == "testing_model"
    assert ext_base_view["sql_table_name"] == "`prod.support_interactions`"
    num_filter_field = next((f for f in ext_base_view["fields"] if f["name"] == "total_count"))
    num_filter_field["filters"][0]["value"] == "1"

    with pytest.raises(StopIteration):
        next((f for f in ext_base_view["fields"] if f["name"] == "avg_hold_time"))

    ext_support_interactions = next(v for v in views if v["name"] == "ext_support_interactions")

    # This is hidden because extension is required
    assert ext_support_interactions["hidden"] is True
    assert ext_support_interactions["model_name"] == "testing_model"
    assert ext_support_interactions["sql_table_name"] == "`prod.support_interactions`"
    assert next((f for f in ext_support_interactions["fields"] if f["name"] == "total_count"))
    assert next((f for f in ext_support_interactions["fields"] if f["name"] == "total_unique_scores"))
    assert next((f for f in ext_support_interactions["fields"] if f["name"] == "avg_hold_time"))
    override_field = next((f for f in ext_support_interactions["fields"] if f["name"] == "confidence_score"))
    assert override_field["type"] == "number"
    assert override_field["sql"] == "SAFE_CAST(${TABLE}.confidence_score as NUMERIC)"

    assert len(models) == 1
    assert models[0]["name"] == "testing_model"

    assert len(topics) == 3
    assert topics[0]["name"] == "user_view"
    assert topics[1]["name"] == "all_visitors_view"
    assert topics[2]["name"] == "zendesk_tickets"

    assert len(views) == 12
    assert views[0]["name"] == "last_touch_attribution_view"

    assert len(dashboards) == 3
    assert dashboards[0]["name"] == "funnel_conversion_data"
    assert dashboards[2]["name"] == "monthly_kpis_dashboard"
    assert dashboards[2]["label"] == "Monthly KPIs Dashboard"

    assert dashboards[2]["filters"] == [
        {"field": "user_view.is_test", "name": "Is Test (Yes / No)", "value": False}
    ]

    assert dashboards[2]["elements"][0]["type"] == "markdown"
    assert dashboards[2]["elements"][0]["size"] == "quarter"
    assert dashboards[2]["elements"][0]["model"] == "testing_model"
    assert dashboards[2]["elements"][0]["content"] == "[MRR](https://google.com)"

    # Make sure this one is ordered correctly, last
    assert dashboards[2]["elements"][-1]["title"] == "New Web Visitors"

    assert dashboards[2]["elements"][1]["title"] == "Total MRR"
    assert dashboards[2]["elements"][1]["plot_options"] == {"grouped_bar": {"display_type": "STACKED"}}
    assert dashboards[2]["elements"][1]["slice_by"] == [
        "profile_facts_view.first_ship_month",
        "last_touch_attribution_view.utm_medium",
    ]

    # Remove the empty filters
    assert len(dashboards[2]["elements"][-1]["filters"]) == 1
    assert dashboards[2]["elements"][-1]["filters"][0]["field"] == "last_touch_attribution_view.utm_content"
    assert dashboards[2]["elements"][-1]["pivot_by"][0] == "last_touch_attribution_view.utm_medium"
    assert dashboards[2]["elements"][-1]["sort"][0] == {
        "field": "last_touch_attribution_view.utm_medium",
        "value": "asc",
    }
    assert dashboards[2]["elements"][-1]["table_calculations"][0] == {
        "title": "Total MoM",
        "formula": "sum([last_touch_attribution_view.count])/offset(sum([last_touch_attribution_view.count]),1)\n-1",  # noqa
        "format": "percent_1",
    }

    assert dashboards[2]["elements"][1]["listen"] == {"Months": "profile_facts_view.first_ship_month"}
    assert "listen" not in dashboards[2]["elements"][3]

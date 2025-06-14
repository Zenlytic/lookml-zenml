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

    # print(models)
    # print()
    # print(views)
    # print()
    # print(dashboards)

    assert len(models) == 1
    assert models[0]["name"] == "testing_model"

    assert len(views) == 9
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

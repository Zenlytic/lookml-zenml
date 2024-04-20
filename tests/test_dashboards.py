import pytest
import yaml
import os
from .conftest import DATA_MODEL_DIRECTORY
from lookml_zenml.lookml_project import LookMLProject


@pytest.mark.unit
def test_convert_dashboard():
    path = os.path.join(DATA_MODEL_DIRECTORY, "dashboards/conversion_dashboard.dashboard.lkml")
    with open(path, "r") as file:
        lkml_result = yaml.safe_load(file)

    print(lkml_result[0])
    project = LookMLProject()
    # All results will be tagged as dimensions because we don't have any views to reference
    result = project.convert_dashboard(lkml_result[0])

    print()
    print()
    print(result)
    assert result["version"] == 1
    assert result["type"] == "dashboard"
    assert result["name"] == "conversion_rates"
    assert result["label"] == "Conversion Rates"
    element = result["elements"][0]

    assert element["model"] == "testing_model"
    assert element["metrics"] == []
    assert element["slice_by"] == [
        "permanent_session_view.count_distinct_sessions",
        "permanent_session_view.session_date_month",
        "visitors_view.total_quiz_starts",
    ]
    assert element["filters"] == [
        {"field": "permanent_session_view.session_date_date", "value": "12 months ago for 12 months"},
        {"field": "permanent_session_view.entry_page", "value": "-%blog%"},
        {"field": "permanent_session_view.is_bot", "value": False},
    ]
    assert element["sort"] == [{"field": "permanent_session_view.session_date_month", "value": "desc"}]
    assert not element["show_annotations"]
    assert element["row_limit"] == 500
    assert element["plot_type"] == "multi_line"

    table_calc_element = result["elements"][-1]

    # This is not correct, but this test shows we do NOT support the custom measures / dimensions yet
    assert table_calc_element["table_calculations"][0] == {
        "format": "percent_2",
        "formula": "[total_converted]/[count_joined]",
        "title": "bottom of funnel",
    }


@pytest.mark.unit
def test_convert_dashboard_funnel():
    path = os.path.join(DATA_MODEL_DIRECTORY, "dashboards/funnel_dashboard.dashboard.lkml")
    with open(path, "r") as file:
        lkml_result = yaml.safe_load(file)

    print(lkml_result[0])
    project = LookMLProject()
    # All results will be tagged as dimensions because we don't have any views to reference
    result = project.convert_dashboard(lkml_result[0])

    print()
    print()
    print(result)
    assert result["version"] == 1
    assert result["type"] == "dashboard"
    assert result["name"] == "funnel_conversion_data"
    assert result["label"] == "Funnel Conversion Data"

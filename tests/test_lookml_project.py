import pytest
from .conftest import ALL_FIELDS_DIRECTORY, DATA_MODEL_DIRECTORY
from lookml_zenml.lookml_project import LookMLProject


@pytest.mark.unit
def test_lookml_project_load():
    project = LookMLProject()
    project_dict = project.load(in_directory=ALL_FIELDS_DIRECTORY)

    assert project_dict["models"][0]["name"] == "model_with_all_fields"
    assert project_dict["models"][0]["connection"] == "connection_name"
    assert project_dict["views"][0]["name"] == "view_name"
    assert project_dict["dashboards"][0]["title"] == "Funnel Conversion Data"


@pytest.mark.unit
def test_lookml_project_convert_project():
    project = LookMLProject()
    project_dict = project.load(in_directory=DATA_MODEL_DIRECTORY)

    models, views, dashboards = project.convert_project(project_dict)

    print(models)
    print()
    print(views)
    print()
    print(dashboards)

    assert len(models) == 1
    assert models[0]["name"] == "testing_model"

    assert len(views) == 9
    assert views[0]["name"] == "last_touch_attribution_view"

    assert len(dashboards) == 2
    assert dashboards[0]["name"] == "funnel_conversion_data"

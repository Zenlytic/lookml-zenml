from .conftest import ALL_FIELDS_DIRECTORY
from lookml_zenml.lookml_project import LookMLProject


def test_lookml_project_load():
    project = LookMLProject(directory=ALL_FIELDS_DIRECTORY)
    project_dict = project.load()

    assert project_dict["models"][0]["name"] == "model_with_all_fields"
    assert project_dict["models"][0]["connection"] == "connection_name"
    assert project_dict["views"][0]["name"] == "view_name"
    assert project_dict["dashboards"][0]["title"] == "Conversion Rates"


def test_lookml_project_convert_project():
    project = LookMLProject(directory=ALL_FIELDS_DIRECTORY)
    # project_dict = project.load()

    # assert project_dict["models"][0]["name"] == "model_with_all_fields"
    # assert project_dict["models"][0]["connection"] == "connection_name"
    # assert project_dict["views"][0]["name"] == "view_name"
    # assert project_dict["dashboards"][0]["title"] == "Conversion Rates"
    assert False


def test_lookml_project_dump():
    project = LookMLProject(directory=ALL_FIELDS_DIRECTORY)
    # project_dict = project.load()

    # assert project_dict["models"][0]["name"] == "model_with_all_fields"
    # assert project_dict["models"][0]["connection"] == "connection_name"
    # assert project_dict["views"][0]["name"] == "view_name"
    # assert project_dict["dashboards"][0]["title"] == "Conversion Rates"
    assert False

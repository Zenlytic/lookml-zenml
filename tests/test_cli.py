import pytest
import lkml
import os
from .conftest import DATA_MODEL_DIRECTORY
from lookml_zenml.lookml_project import LookMLProject


@pytest.mark.cli
def test_convert_dashboard_cli():
    path = os.path.join(DATA_MODEL_DIRECTORY, "conversion_dashboard.dashboard.lookml")
    with open(path, "r") as file:
        lkml_result = lkml.load(file)

    print(lkml_result)
    result = LookMLProject.convert_dashboard(lkml_result)

    assert False


@pytest.mark.cli
def test_convert_model_cli():
    path = os.path.join(DATA_MODEL_DIRECTORY, "conversion_dashboard.dashboard.lookml")
    with open(path, "r") as file:
        lkml_result = lkml.load(file)

    print(lkml_result)
    result = LookMLProject.convert_dashboard(lkml_result)

    assert False


@pytest.mark.cli
def test_convert_view_cli():
    path = os.path.join(DATA_MODEL_DIRECTORY, "conversion_dashboard.dashboard.lookml")
    with open(path, "r") as file:
        lkml_result = lkml.load(file)

    print(lkml_result)
    result = LookMLProject.convert_dashboard(lkml_result)

    assert False


@pytest.mark.cli
def test_convert_project_cli():
    path = os.path.join(DATA_MODEL_DIRECTORY, "conversion_dashboard.dashboard.lookml")
    with open(path, "r") as file:
        lkml_result = lkml.load(file)

    print(lkml_result)
    result = LookMLProject.convert_dashboard(lkml_result)

    assert False

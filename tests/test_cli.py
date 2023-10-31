import os

import pytest
from click.testing import CliRunner

from lookml_zenml.cli import view, model, dashboard, convert


from .conftest import DATA_MODEL_DIRECTORY
from lookml_zenml.lookml_project import LookMLProject


@pytest.mark.cli
def test_convert_dashboard_cli():
    path = os.path.join(DATA_MODEL_DIRECTORY, "dashboards/conversion_dashboard.dashboard.lkml")

    runner = CliRunner()
    result = runner.invoke(dashboard, [path, "--directory", DATA_MODEL_DIRECTORY])

    print(result)
    print(result.output)
    assert '{"version": 1, "type": "dashboard", "name": "conversion_rates"' in result.output
    assert result.exit_code == 0


@pytest.mark.cli
def test_convert_model_cli():
    path = os.path.join(DATA_MODEL_DIRECTORY, "testing_model.model.lookml")
    runner = CliRunner()
    result = runner.invoke(model, [path])

    print(result)
    print(result.output)
    assert '"type": "model", "name": "testing_model", "connection": "testing-snowflake"' in result.output
    assert result.exit_code == 0


@pytest.mark.cli
def test_convert_view_cli():
    path = os.path.join(DATA_MODEL_DIRECTORY, "views/orders_view.view.lkml")
    runner = CliRunner()
    result = runner.invoke(view, [path])

    print(result)
    print(result.output)
    assert '"type": "view", "name": "orders_view", "model_name": "TODO add model name"' in result.output
    assert result.exit_code == 0


@pytest.mark.cli
def test_convert_project_cli(monkeypatch):
    yaml_dump_called = False

    def assert_called(out_directory, models, views, dashboards):
        nonlocal yaml_dump_called
        yaml_dump_called = True
        assert isinstance(models, list)
        assert isinstance(views, list)
        assert isinstance(dashboards, list)
        assert out_directory == "temp/"

    monkeypatch.setattr(LookMLProject, "dump", assert_called)
    runner = CliRunner()
    result = runner.invoke(convert, [DATA_MODEL_DIRECTORY, "--out_directory", "temp/"])

    print(result)
    print(result.output)
    assert yaml_dump_called
    assert result.exit_code == 0

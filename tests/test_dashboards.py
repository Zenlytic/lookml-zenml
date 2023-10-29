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
    result = LookMLProject().convert_dashboard(lkml_result[0])

    print()
    print()
    print(result)
    assert False
    assert result["version"] == 1
    assert result["type"] == "model"
    assert result["name"] == "testing_model"
    assert result["connection"] == "testing-snowflake"
    assert result["access_grants"] == [
        {
            "name": "test_access_grant",
            "user_attribute": "user_attribute_name",
            "allowed_values": ["value_1", "value_2"],
        }
    ]
    assert "includes" not in result

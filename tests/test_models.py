import pytest
import lkml
import os
from .conftest import DATA_MODEL_DIRECTORY
from lookml_zenml.lookml_project import LookMLProject


@pytest.mark.unit
def test_parse_model_from_file_path():
    path = os.path.join(DATA_MODEL_DIRECTORY, "testing_model.model.lookml")
    with open(path, "r") as file:
        lkml_result = lkml.load(file)
        lkml_result["name"] = "testing_model"

    print(lkml_result)
    result = LookMLProject.convert_model(lkml_result, generate_view_metadata=False)

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

    metadata_result = LookMLProject.convert_model(lkml_result, generate_view_metadata=True)
    view_metadata = metadata_result["view_metadata"]

    print(view_metadata)

    assert False

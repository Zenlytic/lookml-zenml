import pytest
import lkml
import os
from .conftest import DATA_MODEL_DIRECTORY
from lookml_zenml.lookml_project import LookMLProject


@pytest.mark.unit
def test_convert_model():
    path = os.path.join(DATA_MODEL_DIRECTORY, "testing_model.model.lookml")
    with open(path, "r") as file:
        lkml_result = lkml.load(file)
        lkml_result["name"] = "testing_model"

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


@pytest.mark.unit
def test_convert_model_join_resolution():
    path = os.path.join(DATA_MODEL_DIRECTORY, "testing_model.model.lookml")
    with open(path, "r") as file:
        lkml_result = lkml.load(file)
        lkml_result["name"] = "testing_model"

    metadata_result = LookMLProject.convert_model(lkml_result, generate_view_metadata=True)
    view_metadata = metadata_result["view_metadata"]

    print(view_metadata)

    assert view_metadata["user_view"] == [
        {"name": "profile_id", "type": "primary", "sql": "${id}"},
        {"name": "email", "type": "primary", "sql": "${email}"},
    ]
    assert view_metadata["profile_facts_view"] == [
        {"name": "profile_id", "type": "primary", "sql": "${profile_id}"}
    ]
    assert view_metadata["orders_view"] == [
        {"name": "profile_id", "type": "foreign", "sql": "${profile_id}"},
        {"name": "orderdatetime_date", "type": "foreign", "sql": "${orderdatetime_date}"},
    ]
    assert view_metadata["session_to_profile_view"] == [
        {"name": "profile_id", "type": "foreign", "sql": "${user_id}"},
        {"name": "session_id", "type": "primary", "sql": "${session}"},
    ]
    assert view_metadata["zendesk_users"] == [
        {"name": "email", "type": "primary", "sql": "${email}"},
        {"name": "requester_id", "type": "primary", "sql": "${user_id}"},
    ]
    assert view_metadata["last_touch_attribution_view"] == [
        {"name": "profile_id", "type": "primary", "sql": "${profile_id}"}
    ]
    assert view_metadata["marketing_spend_daily"] == [
        {"name": "orderdatetime_date", "type": "foreign", "sql": "${date_date}"}
    ]
    assert view_metadata["all_visitors_view"] == [
        {"name": "session_id", "type": "primary", "sql": "${session_id}"}
    ]
    assert view_metadata["zendesk_tickets"] == [
        {"name": "requester_id", "type": "primary", "sql": "${requester_id}"}
    ]

import pytest
import lkml
import os
from .conftest import DATA_MODEL_DIRECTORY
from lookml_zenml.lookml_project import LookMLProjectConverter
from lookml_zenml.lookml_models import LookMLModel, LookMLJoin


@pytest.mark.unit
def test_convert_model():
    path = os.path.join(DATA_MODEL_DIRECTORY, "testing_model.model.lookml")
    with open(path, "r") as file:
        lkml_result = lkml.load(file)
        lkml_result["name"] = "testing_model"

    result = LookMLProjectConverter.convert_model(
        LookMLModel.from_dict(lkml_result), generate_view_metadata=False
    )

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

    metadata_result = LookMLProjectConverter.convert_model(
        LookMLModel.from_dict(lkml_result), generate_view_metadata=True
    )
    view_metadata = metadata_result["view_metadata"]["graph"]

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
    assert view_metadata["session_to_profile"] == [
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
    assert view_metadata["all_visitors"] == [
        {"name": "session_id", "type": "primary", "sql": "${session_id}"}
    ]
    assert view_metadata["zendesk_tickets"] == [
        {"name": "requester_id", "type": "primary", "sql": "${requester_id}"}
    ]


@pytest.mark.unit
def test_lookml_join_sql_where_behavior():
    """Test that LookMLJoin.from_dict correctly combines sql_where and sql_on conditions."""

    # Test case 1: Both sql_where and sql_on present
    join_data_with_both = {
        "name": "test_join",
        "sql_on": "${table_a.id} = ${table_b.id}",
        "sql_where": "${table_b.status} = 'active'",
        "type": "left_outer",
        "relationship": "one_to_one",
    }

    join = LookMLJoin.from_dict(join_data_with_both)

    # The sql_on should now contain the original sql_on plus " AND " plus sql_where
    expected_sql_on = "${table_a.id} = ${table_b.id} AND ${table_b.status} = 'active'"
    assert join.sql_on == expected_sql_on
    assert join.name == "test_join"
    assert join.type == "left_outer"
    assert join.relationship == "one_to_one"

    # Test case 2: Only sql_on present (sql_where should not affect it)
    join_data_only_sql_on = {
        "name": "test_join_2",
        "sql_on": "${table_a.id} = ${table_b.id}",
        "type": "inner",
        "relationship": "many_to_one",
    }

    join2 = LookMLJoin.from_dict(join_data_only_sql_on)

    # sql_on should remain unchanged
    assert join2.sql_on == "${table_a.id} = ${table_b.id}"
    assert join2.name == "test_join_2"

    # Test case 3: Only sql_where present (no sql_on to combine with)
    join_data_only_sql_where = {
        "name": "test_join_3",
        "sql_where": "${table_b.status} = 'active'",
        "type": "left_outer",
        "relationship": "one_to_many",
    }

    join3 = LookMLJoin.from_dict(join_data_only_sql_where)

    # sql_on should be None since there was no original sql_on
    assert join3.sql_on is None
    assert join3.name == "test_join_3"

    # Test case 4: Complex expressions in both sql_where and sql_on
    join_data_complex = {
        "name": "complex_join",
        "sql_on": "${users.id} = ${orders.user_id} AND ${orders.created_date} >= '2023-01-01'",
        "sql_where": "${orders.status} IN ('completed', 'shipped') AND ${orders.amount} > 0",
        "type": "left_outer",
        "relationship": "one_to_many",
    }

    join4 = LookMLJoin.from_dict(join_data_complex)

    expected_complex_sql_on = (
        "${users.id} = ${orders.user_id} AND ${orders.created_date} >= '2023-01-01' AND "
        "${orders.status} IN ('completed', 'shipped') AND ${orders.amount} > 0"
    )
    assert join4.sql_on == expected_complex_sql_on
    assert join4.name == "complex_join"


@pytest.mark.unit
def test_lookml_join_field_replacement_with_sql_where():
    """Test that field replacement works correctly with sql_where when combined with sql_on."""

    # Test with alias mapping
    alias_to_view_mapping = {"orders": "order_facts", "users": "user_profile"}

    join_data = {
        "name": "orders",
        "from": "order_facts",  # This creates the alias mapping
        "sql_on": "${users.profile_id} = ${orders.user_id}",
        "sql_where": "${orders.is_deleted} = FALSE",
        "type": "left_outer",
        "relationship": "one_to_many",
    }

    join = LookMLJoin.from_dict(join_data, alias_to_view_mapping)

    # Fields should be replaced with proper view names
    expected_sql_on = (
        "${user_profile.profile_id} = ${order_facts.user_id} AND ${order_facts.is_deleted} = FALSE"
    )
    assert join.sql_on == expected_sql_on

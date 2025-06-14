import pytest
from .conftest import DATA_MODEL_DIRECTORY
from lookml_zenml.lookml_project import LookMLProjectConverter
from lookml_zenml.lookml_models import LookMLExplore, LookMLExploreFrom


@pytest.mark.unit
def test_convert_project_returns_topics():
    """Test that convert_project returns topics as the fourth element."""
    project = LookMLProjectConverter()
    project_dict = project.load(in_directory=DATA_MODEL_DIRECTORY)

    result = project.convert_project(project_dict)

    # Should return 4 elements: models, views, dashboards, topics
    assert len(result) == 4
    models, views, dashboards, topics = result

    assert isinstance(topics, list)
    assert len(topics) > 0


@pytest.mark.unit
def test_topic_conversion_basic_structure():
    """Test that topics have the correct basic structure."""
    project = LookMLProjectConverter()
    project_dict = project.load(in_directory=DATA_MODEL_DIRECTORY)

    models, views, dashboards, topics = project.convert_project(project_dict)

    # Should have 3 explores from the test model
    assert len(topics) == 3

    # Check basic structure of first topic
    topic = topics[0]
    assert topic["version"] == 1
    assert topic["type"] == "topic"
    assert "name" in topic
    assert topic["model_name"] == "testing_model"


@pytest.mark.unit
def test_topic_names_and_labels():
    """Test that topic names and labels are correctly converted."""
    project = LookMLProjectConverter()
    project_dict = project.load(in_directory=DATA_MODEL_DIRECTORY)

    models, views, dashboards, topics = project.convert_project(project_dict)

    # Find specific topics by name
    user_topic = next(t for t in topics if t["name"] == "user_view")
    sessions_topic = next(t for t in topics if t["name"] == "all_visitors_view")
    zendesk_topic = next(t for t in topics if t["name"] == "zendesk_tickets")

    # Check labels
    assert user_topic["label"] == "Signed in Users"
    assert sessions_topic["label"] == "Sessions"
    assert zendesk_topic["label"] == "Zendesk"


@pytest.mark.unit
def test_topic_base_view_mapping():
    """Test that base_view is correctly mapped from explore from/view_name."""
    project = LookMLProjectConverter()
    project_dict = project.load(in_directory=DATA_MODEL_DIRECTORY)

    models, views, dashboards, topics = project.convert_project(project_dict)

    # Find specific topics
    user_topic = next(t for t in topics if t["name"] == "user_view")
    sessions_topic = next(t for t in topics if t["name"] == "all_visitors_view")
    zendesk_topic = next(t for t in topics if t["name"] == "zendesk_tickets")

    # user_view explore doesn't have 'from', so base_view should be the explore name
    assert user_topic["base_view"] == "user_view"

    # all_visitors_view explore has 'from: all_visitors', so base_view should be 'all_visitors'
    assert sessions_topic["base_view"] == "all_visitors"

    # zendesk_tickets explore doesn't have 'from', so base_view should be the explore name
    assert zendesk_topic["base_view"] == "zendesk_tickets"


@pytest.mark.unit
def test_topic_joins_conversion():
    """Test that joins are correctly converted to views structure."""
    project = LookMLProjectConverter()
    project_dict = project.load(in_directory=DATA_MODEL_DIRECTORY)

    models, views, dashboards, topics = project.convert_project(project_dict)

    # Find user_view topic which has multiple joins
    user_topic = next(t for t in topics if t["name"] == "user_view")

    assert "views" in user_topic
    views_config = user_topic["views"]

    # Should have joins for profile_facts_view, orders_view, lta_view, marketing_spend_daily
    expected_joins = ["profile_facts_view", "orders_view", "lta_view", "marketing_spend_daily"]
    for join_name in expected_joins:
        assert join_name in views_config
        assert "join" in views_config[join_name]
        join_config = views_config[join_name]["join"]
        assert "join_type" in join_config
        assert "relationship" in join_config
        assert "sql_on" in join_config

    # Check specific join configurations
    profile_join = views_config["profile_facts_view"]["join"]
    assert profile_join["join_type"] == "left_outer"
    assert profile_join["relationship"] == "one_to_one"
    assert "${user_view.id} = ${profile_facts_view.profile_id}" in profile_join["sql_on"]

    orders_join = views_config["orders_view"]["join"]
    assert orders_join["join_type"] == "left_outer"
    assert orders_join["relationship"] == "one_to_many"


@pytest.mark.unit
def test_topic_access_grants():
    """Test that required_access_grants are preserved."""
    # Create a mock explore with access grants
    explore_data = {"name": "test_explore", "required_access_grants": ["grant1", "grant2"]}
    explore = LookMLExplore.from_dict(explore_data)

    topic = LookMLProjectConverter.convert_topic(explore, "test_model")

    assert topic["required_access_grants"] == ["grant1", "grant2"]


@pytest.mark.unit
def test_topic_hidden_conversion():
    """Test that hidden field is correctly converted from string to boolean."""
    # Test hidden = "yes"
    explore_data = {"name": "test_explore", "hidden": "yes"}
    explore = LookMLExplore.from_dict(explore_data)
    topic = LookMLProjectConverter.convert_topic(explore, "test_model")
    assert topic["hidden"] is True

    # Test hidden = "no"
    explore_data = {"name": "test_explore", "hidden": "no"}
    explore = LookMLExplore.from_dict(explore_data)
    topic = LookMLProjectConverter.convert_topic(explore, "test_model")
    assert topic["hidden"] is False

    # Test hidden = True (boolean)
    explore_data = {"name": "test_explore"}
    explore = LookMLExplore.from_dict(explore_data)
    topic = LookMLProjectConverter.convert_topic(explore, "test_model")
    assert "hidden" not in topic


@pytest.mark.unit
def test_topic_unsupported_features_raise_errors():
    """Test that unsupported features raise NotImplementedError."""
    # Test extends
    explore_data = {"name": "test_explore", "extends": ["base_explore"]}
    explore = LookMLExplore.from_dict(explore_data)

    with pytest.raises(NotImplementedError, match="Extends are not supported in ZenML"):
        LookMLProjectConverter.convert_topic(explore, "test_model")

    # Test extension
    explore_data = {"name": "test_explore", "extension": "required"}
    explore = LookMLExplore.from_dict(explore_data)

    with pytest.raises(NotImplementedError, match="Extension is not supported in ZenML"):
        LookMLProjectConverter.convert_topic(explore, "test_model")


@pytest.mark.unit
def test_topic_unsupported_features_print_warnings(capsys):
    """Test that unsupported features print warning messages."""
    # Test fields restriction
    explore_data = {"name": "test_explore", "fields": ["field1", "field2"]}
    explore = LookMLExplore.from_dict(explore_data)

    LookMLProjectConverter.convert_topic(explore, "test_model")
    captured = capsys.readouterr()
    assert "Field restriction is not supported in ZenML" in captured.out
    assert "test_explore" in captured.out

    # Test sql_always_where
    explore_data = {"name": "test_explore", "sql_always_where": "1=1"}
    explore = LookMLExplore.from_dict(explore_data)

    LookMLProjectConverter.convert_topic(explore, "test_model")
    captured = capsys.readouterr()
    assert "SQL always where is not supported in ZenML" in captured.out

    # Test conditionally_filter
    explore_data = {
        "name": "test_explore",
        "conditionally_filter": {"filters": [{"field": "test", "value": "test"}]},
    }
    explore = LookMLExplore.from_dict(explore_data)

    LookMLProjectConverter.convert_topic(explore, "test_model")
    captured = capsys.readouterr()
    assert "Conditionally filter is not supported in ZenML" in captured.out

    # Test sql_table_name
    explore_data = {"name": "test_explore", "sql_table_name": "custom_table"}
    explore = LookMLExplore.from_dict(explore_data)

    LookMLProjectConverter.convert_topic(explore, "test_model")
    captured = capsys.readouterr()
    assert "SQL table name is not supported in ZenML" in captured.out


@pytest.mark.unit
def test_topic_from_field_handling():
    """Test different scenarios for the 'from' field handling."""
    # Test with from field
    explore_data = {"name": "test_explore", "from": "custom_view"}
    explore = LookMLExplore.from_dict(explore_data)

    topic = LookMLProjectConverter.convert_topic(explore, "test_model")
    assert topic["base_view"] == "custom_view"

    # Test with view_name
    explore_data = {"name": "test_explore", "view_name": "custom_view_name"}
    explore = LookMLExplore.from_dict(explore_data)

    topic = LookMLProjectConverter.convert_topic(explore, "test_model")
    assert topic["base_view"] == "custom_view_name"

    # Test with neither (should default to explore name)
    explore_data = {"name": "test_explore"}
    explore = LookMLExplore.from_dict(explore_data)

    topic = LookMLProjectConverter.convert_topic(explore, "test_model")
    assert topic["base_view"] == "test_explore"


@pytest.mark.unit
def test_topic_always_filter_conversion():
    """Test that always_filter is correctly converted."""
    explore_data = {
        "name": "test_explore",
        "always_filter": {"filters": [{"field": "test_field", "value": "test_value"}]},
    }
    explore = LookMLExplore.from_dict(explore_data)

    topic = LookMLProjectConverter.convert_topic(explore, "test_model")

    assert "always_filter" in topic
    assert topic["always_filter"]["filters"][0]["field"] == "test_field"
    assert topic["always_filter"]["filters"][0]["value"] == "test_value"


@pytest.mark.unit
def test_topic_access_filter_conversion():
    """Test that access_filter is correctly converted."""
    explore_data = {
        "name": "test_explore",
        "access_filter": [
            {"field": "field1", "user_attribute": "attr1"},
            {"field": "field2", "user_attribute": "attr2"},
        ],
    }
    explore = LookMLExplore.from_dict(explore_data)

    topic = LookMLProjectConverter.convert_topic(explore, "test_model")

    assert "access_filter" in topic
    assert len(topic["access_filter"]) == 2
    assert topic["access_filter"][0]["field"] == "field1"
    assert topic["access_filter"][0]["user_attribute"] == "attr1"


@pytest.mark.unit
def test_topic_label_fallback():
    """Test that label falls back to formatted name when not provided."""
    explore_data = {"name": "test_explore_name"}
    explore = LookMLExplore.from_dict(explore_data)

    topic = LookMLProjectConverter.convert_topic(explore, "test_model")

    # Should create a title-case label from the name
    assert topic["label"] == "Test Explore Name"


@pytest.mark.unit
def test_convert_method_includes_topics():
    """Test that the main convert method properly handles topics."""
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as temp_dir:
        project = LookMLProjectConverter(in_directory=DATA_MODEL_DIRECTORY, out_directory=temp_dir)

        # This should not raise an error and should create topics directory
        project.convert()

        # Check that topics directory was created
        topics_dir = os.path.join(temp_dir, "topics")
        assert os.path.exists(topics_dir)

        # Check that topic files were created
        topic_files = os.listdir(topics_dir)
        assert len(topic_files) == 3  # Should have 3 explores from test model

        # Check file naming convention
        expected_files = ["user_view_topic.yml", "all_visitors_view_topic.yml", "zendesk_tickets_topic.yml"]
        for expected_file in expected_files:
            assert expected_file in topic_files


@pytest.mark.unit
def test_topic_name_removed_from_yaml_output():
    """Test that the name field is removed from the YAML output."""
    import tempfile
    import os
    import yaml

    with tempfile.TemporaryDirectory() as temp_dir:
        project = LookMLProjectConverter(in_directory=DATA_MODEL_DIRECTORY, out_directory=temp_dir)

        project.convert()

        # Read one of the topic files
        topic_file = os.path.join(temp_dir, "topics", "user_view_topic.yml")
        with open(topic_file, "r") as f:
            topic_content = yaml.safe_load(f)

        # Name should not be in the YAML file (it's in the filename)
        assert "name" not in topic_content
        assert topic_content["type"] == "topic"
        assert topic_content["model_name"] == "testing_model"


@pytest.mark.unit
def test_zenlytic_project_includes_topic_paths():
    """Test that the zenlytic_project.yml includes topic-paths."""
    import tempfile
    import os
    import yaml

    with tempfile.TemporaryDirectory() as temp_dir:
        project = LookMLProjectConverter(in_directory=DATA_MODEL_DIRECTORY, out_directory=temp_dir)

        project.convert()

        # Read the project file
        project_file = os.path.join(temp_dir, "zenlytic_project.yml")
        with open(project_file, "r") as f:
            project_content = yaml.safe_load(f)

        # Should include topic-paths
        assert "topic-paths" in project_content
        assert project_content["topic-paths"] == ["topics"]

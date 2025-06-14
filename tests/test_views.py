import pytest
import lkml
import os
from .conftest import DATA_MODEL_DIRECTORY
from lookml_zenml.lookml_project import LookMLProjectConverter
from lookml_zenml.lookml_models import LookMLView


@pytest.mark.unit
def test_parse_model_from_file_path():
    path = os.path.join(DATA_MODEL_DIRECTORY, "views/orders_view.view.lkml")
    with open(path, "r") as file:
        lkml_result = lkml.load(file)

    lkml_view = lkml_result["views"][0]
    result = LookMLProjectConverter.convert_view(LookMLView.from_dict(lkml_view), model_name="test_model")

    # View level checks
    assert result["version"] == 1
    assert result["type"] == "view"
    assert result["name"] == "orders_view"
    assert "label" not in result
    assert "description" not in result
    assert result["model_name"] == "test_model"
    assert result["required_access_grants"] == []
    assert result["sets"] == []
    assert result["access_filters"] == []
    assert result["identifiers"] == []
    assert result["sql_table_name"] == "`etl.prod_read_replica.orders_view`"
    assert result["default_date"] == "orderdatetime"

    # Make sure fields show up (field level checks)
    assert "fields" in result
    assert isinstance(result["fields"], list)
    assert isinstance(next(f for f in result["fields"] if f["name"] == "id"), dict)
    assert isinstance(next(f for f in result["fields"] if f["name"] == "now"), dict)
    assert isinstance(
        next(f for f in result["fields"] if f["name"] == "distinct_influencer_blog_purchasers"), dict
    )

import lkml
import os
from .conftest import ALL_FIELDS_DIRECTORY
from lookml_zenml.view import LookerView


def test_parse_model_from_file_path():
    path = os.path.join(ALL_FIELDS_DIRECTORY, "views/view_with_all_fields.view.lkml")
    with open(path, "r") as file:
        lkml_result = lkml.load(file)

    result = LookerView(path).view
    assert result == lkml_result

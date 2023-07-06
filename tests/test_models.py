import lkml
import os
from .conftest import ALL_FIELDS_DIRECTORY
from lookml_zenml.model import LookerModel


def test_parse_model_from_file_path():
    path = os.path.join(ALL_FIELDS_DIRECTORY, "model_with_all_fields.model.lkml")
    with open(path, "r") as file:
        lkml_result = lkml.load(file)

    result = LookerModel(path).model
    assert result == lkml_result

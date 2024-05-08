import os
import pytest
from flask import Flask
from unittest.mock import MagicMock
from .api_code_block_with_storage import (
    APICodeBlockWithStorage,
)
from .data_storage_code_block import DataStorageCodeBlock


@pytest.fixture
def app():
    app = Flask(__name__)
    return app


@pytest.fixture
def api_block_with_storage(app):
    os.environ['BISMUTH_AUTH'] = "TEST_AUTH"
    api_block = APICodeBlockWithStorage()
    api_block.app.testing = True
    return api_block


def test_add_route_with_storage(api_block_with_storage):
    mock_data_storage = MagicMock(spec=DataStorageCodeBlock)
    mock_data_storage.retrieve.return_value = {"reponse": "OK"}
    api_block_with_storage.add_route_with_storage("/mock", "GET", mock_data_storage)

    with api_block_with_storage.app.test_client() as client:
        client.get("/mock?key=test")
        mock_data_storage.retrieve.assert_called_with("test")

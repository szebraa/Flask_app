import pytest
from api.app import app as flask_app
from flask import current_app as cur
from api import utils as util

#all these methods can be inferred by other test files to access the capabilities modules

@pytest.fixture
def app():
    return flask_app

@pytest.fixture
def utils():
    return util

@pytest.fixture
def current_app():
    return cur

@pytest.fixture
def client(app):
    return app.test_client()
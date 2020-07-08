# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.testing import FlaskClient
import pytest

@pytest.fixture
def create_app():
    return _create_app

class TestClient(FlaskClient):
    def open(self, *args, **kwargs):
        custom_headers = {
            'Content-Type': 'application/json'
        }
        headers = kwargs.pop('headers', {})
        headers.update(custom_headers)
        kwargs['headers'] = headers
        return super(TestClient, self).open(*args, **kwargs)


@pytest.fixture
def app(create_app):
    app = create_app()
    with app.app_context():
        print('init_database')
        testdata.Schema.init_database()
    yield app
    # Handle after test
    from flask_mongoengine import create_connections, get_connection_settings
    conn_settings = get_connection_settings(app.config)
    db = create_connections(app.config)
    db_name = conn_settings.pop('name')
    db.drop_database(db_name)
    print('drop_database')

@pytest.fixture
def client(app):
    app.test_client_class = TestClient
    return app.test_client()

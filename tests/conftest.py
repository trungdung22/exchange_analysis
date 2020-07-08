# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask.testing import FlaskClient
import pytest

from app import create_app as create_app_fac
from settings import TestConfig
import tests.testdata as testdata



def _create_app_test(*args, **kwargs):
    return create_app_fac(TestConfig)


class TestClient(FlaskClient):
    def open(self, *args, **kwargs):
        custom_headers = {
            'Content-Type': 'application/json'
        }
        headers = kwargs.pop('headers', {})
        headers.update(custom_headers)
        kwargs['headers'] = headers
        return super(TestClient, self).open(*args, **kwargs)


@pytest.fixture(scope='module')
def create_app():
    return _create_app_test


@pytest.fixture(scope='module')
def app(create_app):
    app = create_app()
    with app.app_context():
        print('init_database')
        testdata.init_db()
    yield app
    # Handle after test
    from flask_mongoengine import create_connections, get_connection_settings
    conn_settings = get_connection_settings(app.config)
    db = create_connections(app.config)
    db_name = conn_settings.pop('name')
    db.drop_database(db_name)
    print('drop_database')


@pytest.fixture(scope='module')
def client(app):
    app.test_client_class = TestClient
    return app.test_client()

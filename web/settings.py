# -*- coding: utf-8 -*-
"""Application configuration."""
import os
from datetime import timedelta
from celery.schedules import crontab


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('SECRET', 'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_AUTH_USERNAME_KEY = 'email'
    JWT_AUTH_HEADER_PREFIX = 'Token'
    CORS_ORIGIN_WHITELIST = [
        'http://0.0.0.0:4100',
        'http://localhost:4100',
        'http://0.0.0.0:8000',
        'http://localhost:8000',
        'http://0.0.0.0:5000',
        'http://localhost:5000',
        'http://0.0.0.0:4200',
        'http://localhost:4200',
        'http://0.0.0.0:4000',
        'http://localhost:4000',
    ]
    JWT_HEADER_TYPE = 'Token'
    CELERY_IMPORTS = ('web.tasks.actions')
    CELERY_TIMEZONE = 'UTC'
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'

    CELERYBEAT_SCHEDULE = {
        'test-celery': {
            'task': 'web.tasks.actions.fetch_spread_bucket',
            # Every minute
            'schedule': crontab(minute="*/5"),
        }
    }


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_REDIS_MAX_CONNECTIONS = 5
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'postgresql://localhost/example')
    MONGODB = {
        'db': 'dev',
        'alias': 'default',
        'host': 'mongodb://db/exchange'
    }


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    MONGODB = {
        'db': 'dev',
        'alias': 'default',
        'host': 'mongodb://localhost/exchange'
    }
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(10 ** 6)


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    MONGODB = {
        'db': 'testing',
        'alias': 'default',
        'host': 'mongodb://localhost/test'
    }
    # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    BCRYPT_LOG_ROUNDS = 4

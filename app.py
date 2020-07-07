from flask import Flask
from settings import DevConfig
from web.base.model import db
from extensions import cors, cache, celery

from routings import api_bp


def create_app(config_object=DevConfig):
    app = Flask(__name__.split('.')[0], static_folder="./static/", template_folder='./static/build')
    app.url_map.strict_slashes = False

    app.config.from_object(config_object)
    # app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    # app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    app.config['MONGODB_SETTINGS'] = {
        'db': 'testing',
        'alias': 'default',
        'host': 'mongodb://localhost/exchange'
    }
    register_blueprints(app)
    register_extensions(app)
    return app


def register_blueprints(app):
    """Register Flask blueprints."""
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(api_bp, origins=origins)
    app.register_blueprint(api_bp)


def register_extensions(app):
    with app.app_context():
        cache.init_app(app)
        db.init_app(app)
    celery.conf.update(app.config)
    celery.config_from_object(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')

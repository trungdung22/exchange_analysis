from flask_cors import CORS
from flask_caching import Cache

from celery import Celery
celery = Celery('scheduler', broker='redis://localhost:6379/0')

cache = Cache()
cors = CORS()
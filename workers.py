#!/usr/bin/env python
import os
from app import create_app, celery
from flask.helpers import get_debug_flag
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
from settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app()
app.app_context().push()
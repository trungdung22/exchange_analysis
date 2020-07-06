#!/usr/bin/env python
import os
from app import create_app, celery
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = create_app()
app.app_context().push()
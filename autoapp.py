# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag

from web.app import create_app
from web.settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
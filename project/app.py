import os

from flask  import Flask

import views
from models import database, create_tables
from config import DATABASE


def create_app() -> Flask:
    if not os.path.exists(DATABASE):
        create_tables()

    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    views.init_app(app)

    return app
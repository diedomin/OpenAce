from flask import Flask
import logging
from app.config import Config
from app.logging_config import configure_logging
from app.utils.logging_utils import log_event
from app.routes import register_blueprints


def create_app():
    configure_logging()
    app = Flask(__name__)
    app.config.from_object(Config)
    register_blueprints(app)

    @app.route("/")
    def index():
       log_event("info", "health_check", "core")
       return "OpenAce is running"


    return app

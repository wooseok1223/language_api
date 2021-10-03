# -*- coding: utf-8 -*-
import time

from flask import Flask, g
from config.config import DevelopmentConfig, TestingConfig

from app.settings import FLASK_ENV
from app.extensions import db
from app.language import language_bp
from app.search import search_bp
import logging


logging.basicConfig(level=logging.DEBUG)


config_mapper = {
    "staging": DevelopmentConfig,
    "development": DevelopmentConfig,
    "local": DevelopmentConfig,
}


def create_app(config={}):
    app = Flask(__name__)

    app.config.update(config)
    if app.testing:
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(config_mapper.get(FLASK_ENV, DevelopmentConfig))

    # initialize extensions
    db.init_app(app)

    @app.before_request
    def before_request():
        g.start = time.time()

    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "max-age=300"
        response.headers["Expires"] = "0"
        response.headers["Pragma"] = "no-cache"
        response.headers.add("Access-Control-Allow-Credentials", "true")

        return response

    """Add Blueprints"""
    app.register_blueprint(language_bp, url_prefix="/companies")
    app.register_blueprint(search_bp, url_prefix="/search")

    return app

#!/usr/bin/env python3
import os
from flask import Flask, jsonify
from . import flight, swagger_ui
from flask_swagger import swagger

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/api/1/docs/swagger.json')
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0.0"
        swag['info']['title'] = "Saibot Flight Management API"
        swag['definitions'] = swagger_ui.get_definitions()

        return jsonify(swag)

    app.register_blueprint(flight.bp, url_prefix='/api/1'+flight.bp.url_prefix)
    app.register_blueprint(swagger_ui.bp, url_prefix=swagger_ui.url)

    return app

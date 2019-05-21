import os
from flask import Flask, jsonify
from flask_swagger import swagger
from . import gate, swagger_ui

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
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

    @app.route('/api/1/docs/swagger.json')
    def spec():
        swag = swagger(app)
        swag['info']['version'] = '1.0.0'
        swag['info']['title'] = 'Saibot Gate Management API'
        swag['definitions'] = swagger_ui.get_definitions()

        return jsonify(swag)

    app.register_blueprint(gate.bp, url_prefix = gate.bp.url_prefix)
    app.register_blueprint(swagger_ui.bp, url_prefix = swagger_ui.url)

    return app

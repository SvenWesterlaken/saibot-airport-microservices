from flask import Flask


def create_app(config_class=None, instance_relative_config=True):
    app = Flask(__name__)

    if config_class is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_object(config_class)

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app

# from app import models

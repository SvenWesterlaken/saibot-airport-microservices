from flask import Flask
from config import Config
import os



def create_app(config_class=Config):
    app = Flask(__name__,)

    app.config.from_object(config_class)

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
#
#
# from app import models

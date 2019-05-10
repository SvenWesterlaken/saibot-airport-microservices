from flask import Blueprint

bp = Blueprint('routes', __name__, url_prefix='/api')

from app.routes import airlines
from flask_swagger_ui import get_swaggerui_blueprint
from mongo import schemas
import yaml

url = '/api/1/docs'
api_url = 'http://localhost:5001/api/1/docs/swagger.json'

config = {
    'app_name': "Saibot Flight Management API",
}

def get_definitions():
    definition = {}

    for model, schema in schemas:
        definition[model] = yaml.load(schema)

    return definition


bp = get_swaggerui_blueprint(url, api_url, config=config)

from flask_swagger_ui import get_swaggerui_blueprint
from models import schemas
import yaml

# URL of the swagger UI
url = '/api/1/docs'
# URL of the swagger API
api_url = 'http://localhost:5005/api/1/docs/swagger.json'

config = {
    'app_name': 'Saibot Check-in Counter Management API'
}

def get_definitions():
    definition = {}

    # Convert all defined model schemas into a definition array
    for index, schema in schemas:
        definition[index] = yaml.load(schema)

    return definition

bp = get_swaggerui_blueprint(url, api_url, config = config)

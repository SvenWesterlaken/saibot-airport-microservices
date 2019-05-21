from flask_swagger_ui import get_swaggerui_blueprint

url = '/api/1/docs'
api_url = 'http://localhost:5008/api/1/docs/swagger.json'

config = {
    'app_name': "Saibot Security Management API (Events)",
}


bp = get_swaggerui_blueprint(url, api_url, config=config)

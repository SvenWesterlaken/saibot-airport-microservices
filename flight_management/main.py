#!/usr/bin/env python3

from flaskr import create_app
from rabbitmq import rabbitmq
import mongo, env

app = create_app()

if __name__ == "__main__":
    rabbitmq.connect()
    mongo.init(env.mongo_settings)
    app.run(debug=True, host='0.0.0.0', use_reloader=False)

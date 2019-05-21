#!/usr/bin/env python3

from flaskr import create_app
from rabbitmq import rabbitmq_consumer
from db import r as redis

app = create_app()

if __name__ == "__main__":
    rabbitmq_consumer.start()
    redis.connect()

    app.run(debug=True, host='0.0.0.0', use_reloader=False)
    rabbitmq_consumer.stop()
    rabbitmq_consumer.join()

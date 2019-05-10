from app import create_app
from flask import Flask
from app.rabbitmq import rabbitmq

app = create_app()


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    rabbitmq.connect()
    app.run(host="0.0.0.0", debug="true", use_reloader=False)

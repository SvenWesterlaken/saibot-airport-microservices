from app.routes import bp


@bp.route("/airline")
def hello():
    return "Hello World!"

from app import create_app
from app.models import db as mysql_db
from app.models import populate_db
from app.rabbitmq import rabbitmq_publish
from app.rabbitmq import rabbitmq_consume
from app.rabbitmq import msg_handler
from apiv1 import blueprint as apiv1


app = create_app()
app.register_blueprint(apiv1)

mysql_db.bind(provider=app.config['PROVIDER'], host=app.config['HOST'], user=app.config['USER'],
              passwd=app.config['PASSWD'], db=app.config['DB'])

mysql_db.generate_mapping(create_tables=True)

if __name__ == "__main__":
    rabbitmq_publish.connect()
    populate_db()
    print(app.url_map)
    app.run(host="0.0.0.0", debug="true", use_reloader="false")

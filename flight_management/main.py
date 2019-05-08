#!/usr/bin/env python3

from flaskr import create_app
from models import db as mysql_db
from models import Flight
from pony.orm import *
import env

app = create_app()
mysql_db.bind(**env.mysql_db_settings)
mysql_db.generate_mapping(create_tables=True)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

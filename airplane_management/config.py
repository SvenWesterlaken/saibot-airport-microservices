import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    PROVIDER = 'mysql'
    HOST = os.environ.get('MYSQL_HOST')
    USER = os.environ.get('root')
    PASSWD = os.environ.get('MYSQL_PASS')
    DB = os.environ.get('MYSQL_DB')
    PORT = 3307

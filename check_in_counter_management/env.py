from os import environ as env

def getEnvVariable(name):
    try:
        return env[name]
    except KeyError:
        print('Could not find environment variable:', name)

mysql_db_settings = {
    'provider': 'mysql',
    'host': getEnvVariable('MYSQL_HOST'),
    'user': 'root',
    'passwd': getEnvVariable('MYSQL_PASS'),
    'db': getEnvVariable('MYSQL_DB')
}

from os import environ as env

def getEnvVariable(name):

    try:
        return env[name]
    except KeyError:
        print('Could not find environment variable:', name)

mongo_settings = {
    'host': getEnvVariable('MONGO_HOST'),
    'db': getEnvVariable('MONGO_DB'),
    'serverSelectionTimeoutMS': 5
}

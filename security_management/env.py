from os import environ as env

def getEnvVariable(name):

    try:
        return env[name]
    except KeyError:
        print('Could not find environment variable:', name)

redis_settings = {
    'host': getEnvVariable('REDIS_HOST'),
    'port': getEnvVariable('REDIS_PORT'),
    'db': 0
}

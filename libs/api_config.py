from datetime import datetime
import os

GITHUB_ACCESS_TOKEN = 'GITHUB_ACCESS_TOKEN'
LOCATION = 'LOCATION'
LAST_CREATED_DATE= 'LAST_CREATED_DATE'
LAST_UID = 'LAST_UID'
QUALIFIER= 'QUALIFIER'
LAST_USER = 'LAST_USER'
DEFAULT_LOCATION = 'Hong Kong'

def getDefaultLastCreadtedDate():
    return datetime.strftime(datetime.today(), "%Y-%m-%d")

def get_config_from_env():
    config = {}
    config[GITHUB_ACCESS_TOKEN] = getEnvConfig(GITHUB_ACCESS_TOKEN, None)
    config[LOCATION] = getEnvConfig(GITHUB_ACCESS_TOKEN, DEFAULT_LOCATION)
    config[LAST_CREATED_DATE] = getEnvConfig(LAST_CREATED_DATE, getDefaultLastCreadtedDate())
    config[LAST_UID] = getEnvConfig(LAST_UID, 0)
    config[QUALIFIER] = getEnvConfig(QUALIFIER, '')
    config[LAST_USER] = getEnvConfig(LAST_USER, None)

    return config

def getEnvConfig(key, default):
    return os.environ.get(key) if os.environ.get(key) is not None else default

if __name__ == '__main__':
    print(get_config_from_env())
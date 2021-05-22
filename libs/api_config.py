from datetime import datetime
import os

#api_config.py is used to handle API config param

GITHUB_ACCESS_TOKEN = 'GITHUB_ACCESS_TOKEN'
LOCATION = 'LOCATION'
LAST_CREATED_DATE= 'LAST_CREATED_DATE'
LAST_UID = 'LAST_UID'
QUALIFIER= 'QUALIFIER'
LAST_USER = 'LAST_USER'
DEFAULT_LOCATION = 'Hong Kong'
DEFAULT_LAST_UID = '0'

def getDefaultLastCreadtedDate():
    return datetime.strftime(datetime.today(), "%Y-%m-%d")

def get_config_from_env():
    config = {}
    config[GITHUB_ACCESS_TOKEN] = getEnvConfigParam(GITHUB_ACCESS_TOKEN, None)
    config[LOCATION] = getEnvConfigParam(LOCATION, DEFAULT_LOCATION)
    config[LAST_CREATED_DATE] = getEnvConfigParam(LAST_CREATED_DATE, getDefaultLastCreadtedDate())
    config[LAST_UID] = getEnvConfigParam(LAST_UID, DEFAULT_LAST_UID)
    config[QUALIFIER] = getEnvConfigParam(QUALIFIER, '')
    config[LAST_USER] = getEnvConfigParam(LAST_USER, None)

    return config

def getEnvConfigParam(key, default):
    return default if not os.environ.get(key) else os.environ.get(key)

if __name__ == '__main__':
    print(get_config_from_env())
from datetime import datetime

def next_api_access(gh):
    now = datetime.now()
    next_hour = datetime.fromtimestamp(gh.rate_limiting_resettime)
    seconds = (next_hour - now).total_seconds() + 1
    print('Sleep until %s (%s sec)' % (next_hour, seconds))
    return seconds

from github import Github, RateLimitExceededException
import os, csv, re, time
from datetime import datetime, timedelta

def next_api_access(gh):
    now = datetime.now()
    #next_hour = now + timedelta(hours=1)
    #next_hour = next_hour.replace(minute=0,second=0)
    #print('Sleep until %s' % next_hour)
    #return (next_hour - now).total_seconds()
    next_hour = datetime.fromtimestamp(gh.rate_limiting_resettime)
    seconds = (next_hour - now).total_seconds() + 1
    print('Sleep until %s (%s sec)' % (next_hour, seconds))
    return seconds


def retrieve_users():
    ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN')
    location = os.environ.get('LOCATION')
    if location == None:
        location = 'Hong Kong'
    last_created_date = os.environ.get('LAST_CREATED_DATE')
    if last_created_date == None:
        last_created_date = datetime.strftime(datetime.today(), "%Y-%m-%d")
    last_uid = os.environ.get('LAST_UID')
    if last_uid == None:
        last_uid = 0
    else:
        last_uid = int(last_uid)
    qualifier = os.environ.get('QUALIFIER')
    if qualifier == None:
        qualifier = ''
    last_created = last_created_date
    gh = Github(ACCESS_TOKEN)
    count = 0
    while last_created != '':
        last_created_start = last_created
        query = 'location:"'+ location + '" created:<=' + last_created + qualifier
        print(query)
        results = gh.search_users(query, 'joined', 'desc')
        print(f'Got {results.totalCount} users in {location}')

        if results.totalCount > 0:
            if count == 0:
                with open('%s.csv' % location, 'a', newline='', encoding='utf-8') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter=',',
                                           quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csvwriter.writerow(("id", "login", "name", "location", "twitter_username", "created_at", \
                                        "updated_at", "email", "company", "type", "followers", "following", \
                                        "public_repos", "public_gists", "bio", "blog"))
            for i in results:
                count += 1
                if last_uid > 0 and i.id >= last_uid:
                    reset_time = datetime.fromtimestamp(gh.rate_limiting_resettime)
                    print(f'skipping UID {i.id} (Last UID = {last_uid}) {gh.rate_limiting} {reset_time}')
                    continue
                try:
                    name = i.name.encode('utf-8')
                except AttributeError:
                    name = None
                except RateLimitExceededException:
                    time.sleep(next_api_access(gh))
                    name = i.name.encode('utf-8')
                try:
                    bio = i.bio.encode('utf-8')
                except AttributeError:
                    bio = ''
                try:
                    company = i.company.encode('utf-8')
                except AttributeError:
                    company = ''
                reset_time = datetime.fromtimestamp(gh.rate_limiting_resettime)
                print(f'#{count}: {i.id} {i.login} ({name}) {i.created_at} {gh.rate_limiting} {reset_time}')
                last_created = re.split(' ', "%s" % i.created_at)[0]
                with open('%s.csv' % location, 'a', newline='', encoding='utf-8') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter=',',
                                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csvwriter.writerow((i.id, i.login, name, i.location, i.twitter_username, i.created_at, \
                                        i.updated_at, i.email, company, i.type, i.followers, i.following, \
                                        i.public_repos, i.public_gists, bio, i.blog))
                last_uid = i.id
            if last_created == last_created_start:
                last_created = ''
        else:
            last_created = ''
        print('Last Created: %s' % last_created)

if __name__ == '__main__':
    retrieve_users()


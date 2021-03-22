from github import Github, RateLimitExceededException
import os, csv, re, time
from datetime import datetime
from libs.api import next_api_access
from libs import api_config

def retrieve_users(config):
    accessToken = config[api_config.GITHUB_ACCESS_TOKEN]
    location = config[api_config.LOCATION]
    last_created_date = config[api_config.LAST_CREATED_DATE]
    last_uid = int(config[api_config.LAST_UID])
    qualifier =  config[api_config.QUALIFIER]


    last_created = last_created_date
    gh = Github(accessToken)
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
    config = api_config.get_config_from_env()
    retrieve_users(config)


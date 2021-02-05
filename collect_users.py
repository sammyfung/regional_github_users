from github import Github
#import time
import os, csv, re
from datetime import datetime

def retrieve_users():
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
                try:
                    name = i.name.encode('utf-8')
                except AttributeError:
                    name = None
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
                #print(dir(i))
                #time.sleep(2)
            if last_created == last_created_start:
                last_created = ''
        else:
            last_created = ''
        print('Last Created: %s' % last_created)

if __name__ == '__main__':
    ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN')
    location = 'Hong Kong'
    last_created_date = datetime.strftime(datetime.today(), "%Y-%m-%d")
    qualifier = ''
    retrieve_users()


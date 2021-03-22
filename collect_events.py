from github import Github, RateLimitExceededException, GithubException
import os, csv, time
from datetime import datetime
from libs.api import next_api_access
from libs import api_config

def read_user_db(location):
    with open('%s.csv' % (location), newline='', encoding='utf-8') as csvfile:
        raw_list = {}
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            login = row[1]
            try:
                followers = int(row[10])
            except:
                followers = 0
            raw_list[login] = followers
    return raw_list


def collect_events_for_user(login, accessToken, location):
    gh = Github(accessToken)
    get_success = False
    while (not get_success):
        try:
            results = gh.get_user(login).get_public_events()
            print("Got %s results for %s" % (results.totalCount, login))
            get_success = True
        except RateLimitExceededException:
            time.sleep(next_api_access(gh))
        except GithubException:
            results = []
            get_success = True
    count = 0
    repo_counts = {}
    for i in results:
        get_success = False
        while (not get_success):
            try:
                count += 1
                reset_time = datetime.fromtimestamp(gh.rate_limiting_resettime)
                if i.org != None:
                    org = i.org.login
                else:
                    org = None
                try:
                    commit_count = repo_counts[i.repo.full_name]
                except KeyError:
                    repo_counts[i.repo.full_name] = i.repo.get_commits().totalCount
                    commit_count = repo_counts[i.repo.full_name]
                print(f"#{count} {i.actor.login} {i.created_at} {i.id} {org} {i.repo.owner.login} {i.repo.html_url} Fork?{i.repo.fork} {i.repo.watchers_count} *{i.repo.stargazers_count} {i.repo.forks_count} {i.repo.open_issues_count} {commit_count} {i.repo.language} {i.type} {gh.rate_limiting} {reset_time}")

                with open('%s - events.csv' % (location), 'a', newline='', encoding='utf-8') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter=',',
                                           quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csvwriter.writerow((count, i.actor.login, i.created_at, i.id, org, i.repo.owner.login, \
                                        i.repo.html_url, i.repo.fork, i.repo.watchers_count, \
                                        i.repo.stargazers_count, i.repo.forks_count, i.repo.open_issues_count, \
                                        commit_count, i.repo.language, i.type))
                get_success = True
            except RateLimitExceededException:
                time.sleep(next_api_access(gh))
                continue
            except:
                print(f"#{count} {i.actor.login} {i.created_at} {i.id} {i.type} {gh.rate_limiting} {reset_time}")
                with open('%s - events.csv' % (location), 'a', newline='', encoding='utf-8') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter=',',
                                           quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csvwriter.writerow((count, i.actor.login, i.created_at, i.id, org, '', \
                                        '', '', '', '', '', '', '', '', i.type))
                get_success = True
    print("Counted %s results for " % count)


def collect_events(config):
    accessToken = config[api_config.GITHUB_ACCESS_TOKEN]
    location = config[api_config.LOCATION]
    last_user = config[api_config.LAST_USER]

    new_user = True if last_user is None else False    

    last_created_date = datetime.strftime(datetime.today(), "%Y-%m-%d")
    qualifier = ''

    raw_list = read_user_db(location)
    users = sorted(raw_list.items(), key=lambda i: i[1], reverse=True)

    with open('%s - events.csv' % (location), 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(("count", "login", "created_at", "id", "org", "owner_login", \
                            "html_url", "fork", "watchers_count", \
                            "stargazers_count", "forks_count", "open_issues_count", \
                            "commits_count", "language", "type"))
    no_of_users = 0
    for i in users:
        no_of_users += 1
        if i[0] == last_user:
            new_user = True
        if new_user:
            print('------ %s %s (Followers = %s) ------' % (no_of_users, i[0], i[1]))
            collect_events_for_user(i[0], accessToken, location)
        else:
            print('Skipping %s %s (Followers = %s)'% (no_of_users, i[0], i[1]))

if __name__ == '__main__':
    config = api_config.get_config_from_env()
    collect_events(config)
    


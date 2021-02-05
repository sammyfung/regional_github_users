# regional_github_users

a python script to collect the information of regional github users, the default regional (the location) is Hong Kong.

## Requirements

1. PyGitHub
2. GitHub Access Token

## Run

$ export ACCESS_TOKEN=your_github_access_token

For regional user information.
$ python collect_users.py

Collected user information will be saved to 'Location Name'.csv, ie. Hong Kong.csv for the default location.

For events of regional users in last 3 months. (in development)
(missing in this repos, will be released, or pls contact us)
$ python collect_events.py

Collected public events will be saved to 'Location Name' - events.csv, ie. Hong Kong - events.csv for the default location.

## Todo

Developing a script to collect the public events of regional users in last 3 months (limited by GitHub API).

## Authors

Sammy Fung <sammy@sammy.hk>

# regional_github_users

a python script to collect the information of regional github users using [GitHub API v3](https://docs.github.com/en/rest), the default regional (the location) is Hong Kong.

## Requirements

1. [PyGithub](https://github.com/PyGithub/PyGithub)
2. GitHub Access Token

Installing required python libraries thru requirements.txt

```
$ pip install -r requirements.txt
```

## Run

```
$ export ACCESS_TOKEN=your_github_access_token
```

For regional user information.   

```
$ python collect_users.py
```

Collected user information will be saved to 'Location Name'.csv, ie. Hong Kong.csv for the default location. You can use environment variables to set a custom location before run the program.

```
$ export LOCATION='USA'
```

Other qualifiers for GitHub search users API can be used. Examples:

```
$ export LAST_CREATED_DATE='2019-06-16'

$ export LAST_UID='12345'

$ export QUALIFIER='type:user'
```

For events of regional users in last 3 months.

```
$ python collect_events.py
```

Collected public events will be saved to 'Location Name' - events.csv, ie. Hong Kong - events.csv for the default location.

## Authors

Sammy Fung <sammy@sammy.hk>

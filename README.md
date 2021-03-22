# regional_github_users

a python script to collect the information of regional github users using [GitHub API v3](https://docs.github.com/en/rest), the default regional (the location) is Hong Kong.

## Requirements

1. Python 3.6 or later
2. [PyGithub](https://github.com/PyGithub/PyGithub)
3. [GitHub Access Token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)

Installing required python libraries thru requirements.txt

```
$ pip install -r requirements.txt
```

## Run

It's recommended to generate your GitHub access token and export as an environment variable on Linux/OSX.

```
$ export ACCESS_TOKEN=your_github_access_token
```

### For regional user information   

```
$ python collect_users.py
```

It start to collect from the latest created users in the region. Collected user information will be saved to 'Location Name'.csv, ie. Hong Kong.csv for the default location. You can use other environment variables to set a custom location before run the program.

```
$ export LOCATION='USA'
```

Other qualifiers for GitHub search users API can be used. Examples:

```
$ export LAST_CREATED_DATE='2019-06-16'

$ export LAST_UID='12345'

$ export QUALIFIER='type:user'
```

### For recent public events of regional users

```
$ python collect_events.py
```

You must run the collect_users.py first befure running this script. This script will take the data from CSV files outputted by collect_users.py. 

It start to collect from the most followed users in the region. Only events in recent 3 months will be provided thru GitHub API. 

Collected public events will be saved to 'Location Name' - events.csv, ie. Hong Kong - events.csv for the default location.

### JSON Configuration 
In addition to environment variables, JSON file can be used to set the config. 
(* Config parameters are read from environment variables by default.)
#### Command Line Argument
```
$ python collect_users.py -j <JSON file path>
$ python collect_events.py -j <JSON file path>
```
OR
```
$ python collect_users.py --json <JSON file path>
$ python collect_events.py --json <JSON file path>
```


#### Sample JSON Template
```json
{
    "GITHUB_ACCESS_TOKEN":"",
    "LOCATION":"Hong Kong",
    "LAST_CREATED_DATE":"",
    "LAST_UID":"1",
    "QUALIFIER":"",
    "LAST_USER":""
}
```

## Authors

Sammy Fung <sammy@sammy.hk>

# DevDiaries
This is what we did

## Usage:
    $ mkvirtualenv -p /usr/bin/python3 <env>
    $ workon <env>
    $ pip install -r requirements.txt
    $ python manage.py db init
    $ python manage.py db migrate
    $ python manage.py initdb
    $ python manage.py runserver
    
### To get help:
    $ python manage.py

## TODOs:
    Add search for Link and Tag
    Add moderator category {Link, Video, OFF, ...}
    Forgot password
    Email recovery
    Email confirmation
    Write test (user completed)
    Documentation for all modules, classes and functions -> WIP
    Add logger
    Make admin app
    Fix phone number regex issue
    Fix emial regex issue

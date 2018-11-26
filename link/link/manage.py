#!/usr/bin/env python3
"""Manage Application"""

import os
import subprocess
from flask_migrate import Migrate, MigrateCommand, upgrade
from flask_script import Manager, Shell, Command, Option

from link.models import Link, Tag
from user.models import User, Role, Info
from server import app, db


manager = Manager(app)
migrate = Migrate(app, db)

def _make_context():
    return dict(app=app, db=db, User=User, Role=Role,
                Info=Info, Link=Link, Tag=Tag)


manager.add_command("shell", Shell(make_context=_make_context))
manager.add_command("db", MigrateCommand)


@manager.command
def init_db():
    print("INITIALIZING DATABASE")
    upgrade()
    db.create_all()
    Role.init_roles()


@manager.command
def drop_db():
    print("DROP TABLES")
    db.drop_all()


if __name__ == '__main__':
    try:
        with open('.env', 'r') as fenv:
            for link in fenv.readline:
                key, value = line.split('=')
                os.environ[key] = value
    except Exception as e:
        print("File is missing or variable not matched")
        raise
    manager.run()

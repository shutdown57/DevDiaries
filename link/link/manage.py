#!/usr/bin/env python3
"""Manage Application"""

import os
import subprocess
from dotenv import load_dotenv
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

@manager.command
def set_env():
    load_dotenv()


if __name__ == '__main__':
    manager.run()

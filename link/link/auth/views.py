from flask import render_template, redirect, url_for

from auth import bp_auth
from flask_login import current_user


@bp_auth.route('/register', methods=['GET'])
def register_create():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    return render_template('auth/register.html')


@bp_auth.route('/register', methods=['POST'])
def register_store():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    return redirect(url_for('bp_user.home'))


@bp_auth.route('/login', methods=['GET'])
def login_create():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    return render_template('auth/login.html')


@bp_auth.route('/login', methods=['POST'])
def login_store():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    return redirect(url_for('bp_user.home'))

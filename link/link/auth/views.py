from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user

from auth import bp_auth
from user.models import User
from user.validation import UserValidate
from flask_login import current_user


@bp_auth.route('/register', methods=['GET'])
def register_create():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    return render_template('auth/register.html', user=type(current_user))


@bp_auth.route('/register', methods=['POST'])
def register_store():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    if not request.form['password'] == request.form['password_confirm']:
        flash("Password not matched", "error")
        return redirect(url_for('bp_auth.register_create'))
    if request.form and 'email' in request.form.keys() and \
            'password' in request.form.keys():
        if UserValidate.email(request.form['email']) and \
                UserValidate.password(request.form['password']):
            user = User.create(
                email=request.form['email'],
                password_=request.form['password']
            )
            if user:
                login_user(user, False)
                flash("welcome", "success")
                return redirect(url_for('bp_user.index'))
            flash("Problem with server, try again", "warning")
            return redirect(url_for('bp_auth.register_create'))
        else:
            flash("Someone exists with this email address", "error")
            return redirect(url_for('bp_auth.register_create'))
    flash("Credentials are necessary", "error")
    return redirect(url_for('bp_auth.register_create'))


@bp_auth.route('/login', methods=['GET'])
def login_create():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    return render_template('auth/login.html')


@bp_auth.route('/login', methods=['POST'])
def login_store():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    if not request.form and 'email' in request.form.keys() and \
            'password' in request.form.keys():
        return redirect(url_for('bp_auth.login_create'))
    user = User.query.filter_by(email=request.form['email'])
    if not user and not user.verify_password(request.form['password']):
        flash('email or password is wrong', 'error')
        return redirect(url_for('bp_auth.login_create'))
    remember = request.form['remember'] if 'remember' in request.form.keys() \
        else False
    login_user(user, remember)
    return redirect(url_for('bp_user.index'))

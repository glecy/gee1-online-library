from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect (url_for('main.index'))
    else:
        return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    given_username = request.form.get('user')
    given_password = request.form.get('password')

    user = User.query.filter_by(username=given_username).first()
    if not user or not check_password_hash(user.password, given_password):
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

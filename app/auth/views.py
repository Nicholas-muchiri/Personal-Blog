from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from ..models import User
from .. import db
from ..email import mail_message

@auth.route('/register', methods = ["GET", "POST"])
def register():
    '''
    adds user to db through registration form
    '''
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(fullname = form.fullname.data, username = form.username.data, email = form.email.data, password = form.password.data)

        db.session.add(user)
        db.session.commit()

        mail_message('Welcome to my Blog', 'email/welcome_subscriber', user.email, user = user)

        flash('You have successfully registered! You may now log in.')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', register_form = form, title = 'Register')

@auth.route('/login', methods = ["GET", "POST"])
def login():
    '''
    log the user in through login form
    '''
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember.data)

            if user.is_admin:
                return redirect(url_for('main.dashboard'))

            return redirect(url_for('main.index'))
        
        flash('Invalid email or password.')

    return render_template('auth/login.html', login_form = login_form, title = 'Login')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')

    return redirect(url_for('main.index'))
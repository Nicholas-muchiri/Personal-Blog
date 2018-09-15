from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, SubmitField, ValidationError
from wtforms.validators import Required, Email, EqualTo

from ..models import User

class RegistrationForm(FlaskForm):
    '''
    form for user to create an account
    '''
    fullname = StringField('Full Name', validators = [Required()])
    username = StringField('Username', validators = [Required()])
    email = StringField('Email', validators = [Required(), Email()])
    password = PasswordField('Password', validators = [Required(),
    EqualTo('confirm_password', message = 'Password must match')])
    confirm_password = PasswordField('Confirm Password', validators = [Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email is already taken.')

    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Username is already taken.')

class LoginForm(FlaskForm):
    '''
    form for user to log in
    '''
    email = StringField('Email', validators = [Required(), Email()])
    password = PasswordField('Password', validators = [Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

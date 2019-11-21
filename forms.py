from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError

#after Registration user must be able to login
class LoginForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired(),Email()])
    password = PasswordField('Password',validators = [DataRequired()])
    submit = SubmitField('Log in ')


class RegistrationForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired(),Email()])
    username = StringField('Username',validators = [DataRequired()])
    password = PasswordField('Password',validators = [DataRequired(),EqualTo('pass_confirm',message = 'Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password',validators = [DataRequired()])
    submit = SubmitField('Register!')


    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():  # to check that email has already been registered or not
           raise ValidationError('Your email has been already registered!')


    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():  # to check that username has already been taken or not
           raise ValidationError('Username is taken!')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, InputRequired, EqualTo


class LoginForm(FlaskForm):
    """User Login Form."""
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email(message='Enter a valid email.'),
                            InputRequired(message='Field required')]
                        )
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 Length(min=5, max=25, message='Invalid password'),
                                 InputRequired(message='Field required')]
                             )
    submit = SubmitField('Log In')


class SignupForm(FlaskForm):
    """User Signup Form."""
    username = StringField('Name',
                       validators=[
                           DataRequired(),
                           Length(min=5, max=25, message='Length name range 5 to 25 symbols'),
                           InputRequired(message='Field required')]
                       )
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Length(min=5, max=25),
                            Email(message='Enter a valid email.')]
                        )
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 Length(min=5, max=25, message='Select a stronger password.')]
                             )
    confirm_password = PasswordField('Confirm Your Password',
                                     validators=[
                                         DataRequired(),
                                         InputRequired(message='Field Name required'),
                                         EqualTo('password', message='Passwords must match.')]
                                     )
    submit = SubmitField('Register')


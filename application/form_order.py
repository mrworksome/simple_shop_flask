from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import Length, InputRequired, Email


class OrderForm(FlaskForm):
    """User Order Form."""
    username = StringField('Name',
                           validators=[
                               Length(min=4, max=20, message='Length name range 5 to 25 symbols'),
                               InputRequired(message='Field required')]
                           )
    address = StringField('Address',
                          validators=[
                            Length(min=4, message='Length name range 5 to 25 symbols'),
                            InputRequired(message='Field required')]
                          )
    email = StringField('Email',
                        validators=[
                            Email(message='Email invalid'),
                            InputRequired(message='Field required')]
                        )
    phone = StringField('Phone',
                        validators=[
                            Length(min=4),
                            InputRequired(message='Field required')]
                        )
    price = HiddenField('price')

    submit = SubmitField('Order')

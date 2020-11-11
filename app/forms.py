from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email

class EventsForm(FlaskForm):
    author = StringField('author')
    from_date = DateField('from_date', format='%Y-%m-%d', validators=[DataRequired()])
    to_date = DateField('to_date', format='%Y-%m-%d', validators=[DataRequired()])
    theme = StringField('theme')
    description = TextAreaField('description')

class CreateUserForm(FlaskForm):
    email = StringField('Email:', validators=[Email()])
    password = StringField('Password')
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[Email()])
    password = StringField('Password')
    submit = SubmitField('Войти')
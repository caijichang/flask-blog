from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, URL

#btn-primary
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)], render_kw={'placeholder': 'Your Username', 'class': 'form-control'})
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)], render_kw={'placeholder': 'Your Password', 'class': 'form-control', 'data-eye': 'data-eye'})
    remember = BooleanField('Remember Me')
    # submit = SubmitField('Log in')
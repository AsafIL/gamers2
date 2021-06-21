from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required
from flask_login import current_user


class LoginForm(Form):
    """Accepts a nickname and a room."""
    room = StringField('Room', validators=[Required()])
    submit = SubmitField('Enter Chatroom')
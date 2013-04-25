from wtforms import Form, TextField, PasswordField
from django.utils.translation import ugettext as _

from wtforms.validators import ValidationError
from wtforms import validators
from testing_runtime.models import User
from core import db

def user_exists(form, field):
    user = db.user_session.query( User ).filter( User.username == field.data ).first()
    if user is None:
        raise ValidationError( _( 'User does not exist' ) )


class LoginForm( Form ) :
    username = TextField( _( 'User name' ), validators=[ validators.Required(), user_exists ] )
    password = PasswordField( _( 'Password' ), validators=[ validators.Required() ] )
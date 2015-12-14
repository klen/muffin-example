""" Setup admin interface. """
import muffin
from muffin_admin.peewee import PWAdminHandler

from example import app
from example.models import User, Test


@app.ps.admin.authorization
def authorize(request):
    """ Base authoriazation for every admin handler. Checks for current user's permissions.

    It can be redifined for each handler.

    """
    user = yield from app.ps.session.load_user(request)
    if not user or not user.is_super:
        raise muffin.HTTPFound('/')
    return user


@app.register
class TestAdmin(PWAdminHandler):

    """Simplest example."""

    model = Test


@app.register
class UserAdmin(PWAdminHandler):

    """View registered users."""

    model = User
    columns = 'id', 'created', 'username', 'is_super'
    filters = 'username', 'is_super'
    form_meta = {
        'exclude': ['password'],
    }

    # Disable changes on production
    can_create = can_edit = can_delete = app.cfg.CONFIG == 'example.config.debug'

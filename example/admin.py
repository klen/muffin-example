"""Setup admin interface."""

from muffin import ResponseRedirect
from muffin_admin import Plugin as Admin, PWAdminHandler

from . import app, session
from .models import User, Message


admin = Admin(app)


@admin.check_auth
async def authorize(request):
    """Authorize users to access the admin."""
    user = await session.load_user(request)
    if user and user.is_super:
        return user

    raise ResponseRedirect('/')


@admin.get_identity
async def ident(request):
    """Get an identity for the current user.."""
    user = await session.load_user(request)
    if user:
        return {
            'id': user.id,
            'fullName': user.email,
        }


@admin.dashboard
async def dashboard(request):
    """Render a simple dashboard."""
    return [[{
        'title': 'app config',
        'value': [(k, str(v)) for k, v in app.cfg],
    }]]


@admin.route
class UsersAdmin(PWAdminHandler):
    """Manage users."""

    class Meta:
        """Tune the handler."""

        icon = "People"

        model = User
        filters = 'email', 'is_super'
        schema_meta = {
            'load_only': ('password',),
        }


@admin.route
class MessagesAdmin(PWAdminHandler):
    """Manage messages."""

    class Meta:
        """Tune the handler."""

        icon = "Message"
        references = {'user': 'user.email'}

        model = Message
        filters = 'user',

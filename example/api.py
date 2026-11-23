"""Example API."""
import datetime as dt

from asgi_tools._compat import aio_wait
from marshmallow import fields
from marshmallow_peewee import ModelSchema
from muffin_rest import API, PWRESTHandler

from example import app, session, WEB_SOCKETS
from example.models import Message, User


api = API(app, prefix='/api')


class MSTimestamp(fields.Field):
    """Serialize a datetime as a Unix timestamp in milliseconds."""

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return int(value.replace(tzinfo=dt.UTC).timestamp()) * 1000


class UserSchema(ModelSchema):
    """Serialize message authors without private fields."""

    class Meta:
        """Tune the schema."""

        model = User
        exclude = ('password', 'is_super', 'created')


class MessagesSchema(ModelSchema):
    """Serialize/deserialize messages."""

    created = MSTimestamp(dump_only=True)
    user = fields.Nested(UserSchema, dump_only=True)

    class Meta:
        """Tune the schema."""

        model = Message


@api.route
class Messages(PWRESTHandler):
    """Messages API."""

    methods = 'get', 'post'

    class Meta:
        """Tune the endpoint."""

        model = Message
        limit = 50
        name = 'messages'

        Schema = MessagesSchema

    async def prepare_collection(self, request):
        """Order messages by id."""
        return Message.select(Message, User).join(User, 'LEFT OUTER JOIN').order_by(Message.id)

    async def load(self, request, resource: Message = None) -> Message:
        """Bind user to the message and send notify to sockets."""
        msg = await super().load(request, resource=resource)
        msg.user = await session.load_user(request)
        data = MessagesSchema().dump(msg)
        coros = [ws.send_json({'type': 'msg', 'data': data}) for ws in WEB_SOCKETS]
        await aio_wait(*coros)
        return msg

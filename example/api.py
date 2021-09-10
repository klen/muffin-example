"""Example API."""
from asgi_tools._compat import aio_wait
from marshmallow_peewee import MSTimestamp, ModelSchema, Related
from muffin_rest import API, PWRESTHandler

from example import app, session, WEB_SOCKETS
from example.models import Message, User


api = API(app, prefix='/api')


class MessagesSchema(ModelSchema):
    """Serialize/deserialize messages."""

    created = MSTimestamp(dump_only=True)
    user = Related(dump_only=True, meta={'exclude': ('password', 'is_super', 'created')})

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

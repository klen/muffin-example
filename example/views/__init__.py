"""Setup views."""

# Important: This is just a quick simple example.
# In production everything should be more serious (authentication, work with websockets and etc)

import muffin

from example import WEB_SOCKETS, app, db, jinja2, session


@app.route("/")
async def index(request):
    """Get a current logged user and render a template to HTML."""
    user = await session.load_user(request)
    return await jinja2.render("index.html", user=user, view="index")


@app.route("/ws")
async def websocket(request):
    """Process websockets."""
    user = await session.load_user(request)
    user = user and user.email or "anonimous"

    # Release current connection (from peewee middleware)
    await db.manager.current_conn.release()

    ws = muffin.ResponseWebSocket(request)
    await ws.accept()

    # Notify connected users
    for ws_ in WEB_SOCKETS:
        await ws_.send_json({"type": "join", "data": user})

    WEB_SOCKETS.append(ws)

    while ws.connected:
        await ws.receive()

    WEB_SOCKETS.remove(ws)

    # Notify connected users
    for ws_ in WEB_SOCKETS:
        await ws_.send_json({"type": "disconnect", "data": user})

    # Close socket
    await ws.close()

    return ws


# Import submodules for views
app.import_submodules()

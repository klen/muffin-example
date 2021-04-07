"""Authorization views."""

import muffin

from example import app, session, oauth
from example.models import User, Token


# Setup function to load users from sessions
@session.user_loader
def get_user(user_id):
    """Register a user's loader for sessions."""
    return User.select().where(User.id == user_id).first()


# app.route supports any regexp in paths
@app.route('/login')
async def login(request):
    """Login a user."""
    data = request.url.query or await request.form()
    user = User.select().where(User.email == data.get('email')).first()
    if user and user.check_password(data.get('password')):
        session.login(request, user.id)

    return muffin.ResponseRedirect('/')


@app.route('/logout')
async def logout(request):
    """Logout a user."""
    session.logout(request)
    return muffin.ResponseRedirect('/')


@app.route('/oauth/github')
async def login_with_github(request):
    """Login with Github."""
    client, data, raw = await oauth.login('github', request)
    try:
        token = Token.select().where(Token.token == client.access_token).get()
        user = token.user
    except Exception:
        info = await client.request('GET', 'user')
        user, _ = User.get_or_create(email=info['email'], defaults=dict(
            password='NULL', username=info['login']))

        token, _ = Token.get_or_create(
            user=user, provider='github', defaults=dict(token=client.access_token))

    session.login(request, user.id)
    return muffin.ResponseRedirect('/')

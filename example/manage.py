"""Setup the application's CLI commands."""

from example import app, db


@app.manage
def hello(name, upper=False):
    """Write command help text here.

    :param name:  Write your name
    :param upper: Use uppercase

    """
    greetings = f"Hello {name}!"
    if upper:
        greetings = greetings.upper()
    print(greetings)


@app.manage
async def example_users():
    """Create users for the example."""
    from example.models import User

    async with db.connection():

        await User.get_or_create(email='user@muffin.io', defaults={
            'username': 'user', 'password': User.generate_password('pass'),
        })
        await User.get_or_create(email='admin@muffin.io', defaults={
            'username': 'admin', 'password': User.generate_password('pass'), 'is_super': True,
        })

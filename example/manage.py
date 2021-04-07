"""Setup the application's CLI commands."""

from example import app


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
def example_users():
    """Create users for the example."""
    from mixer.backend.peewee import Mixer
    from example.models import User

    mixer = Mixer(commit=True)
    mixer.guard(User.email == 'user@muffin.io').blend(
        User, email='user@muffin.io', password=User.generate_password('pass'))
    mixer.guard(User.email == 'admin@muffin.io').blend(
        User, email='admin@muffin.io', password=User.generate_password('pass'), is_super=True)

"""Initialize the application and plugins."""

from muffin import Application

from muffin_jinja2 import Plugin as Jinja2
from muffin_oauth import Plugin as OAuth
from muffin_peewee import Plugin as Peewee
from muffin_session import Plugin as Session


# Initialize a muffin application
# -------------------------------
app = Application(

    # Modules to import configuration
    'env:MUFFIN_CONFIG', 'example.config.debug',

    # Application name (it also can be inside configuration modules
    name='example'

)

WEB_SOCKETS = []  # XXX: Just an example

# Initialize plugins
# ------------------
jinja2 = Jinja2(app)      # Jinja Templates
oauth = OAuth(app)        # OAuth (Social) authorization
db = Peewee(app)          # Peewee ORM Support
session = Session(app)    # Cookie Sessions

# Connect submodules (register models, view and etc)
# --------------------------------------------------
app.import_submodules()

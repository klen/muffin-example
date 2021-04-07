# Import the project's settings
from .defaults import *

PEEWEE_CONNECTION = 'sqlite+async:///example.sqlite'
OAUTH_CLIENTS = {
    'github': {
        'client_id': 'b6281b6fe88fa4c313e6',
        'client_secret': '21ff23d9f1cad775daee6a38d230e1ee05b04f7c',
        'scope': 'user:email',
    }
}
OAUTH_REDIRECT_URI = None
JINJA2_AUTO_RELOAD = True
DEBUG = True

# DEBUG = True
LOG_LEVEL = 'DEBUG'

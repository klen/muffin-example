# Import the project's settings
from .production import *

PEEWEE_CONNECTION = 'sqlite:///example.sqlite'
OAUTH_CLIENTS = {
    'github': {
        'client_id': 'b6281b6fe88fa4c313e6',
        'client_secret': '21ff23d9f1cad775daee6a38d230e1ee05b04f7c',
    }
}

# DEBUG = True
LOG_LEVEL = 'DEBUG'

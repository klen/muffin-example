import os

# Gunicorn
# ========
bind = '127.0.0.1:5000'

# Muffin
# ======

PLUGINS = (

    # Contrib plugins
    'muffin_jinja2',
    'muffin_peewee',
    'muffin_session',
    'muffin_oauth',
    'muffin_admin',
)

STATIC_FOLDERS = 'example/static',

# Plugin options
# ==============

SESSION_SECRET = 'SecretHere'
JINJA2_TEMPLATE_FOLDERS = 'example/templates',
OAUTH_CLIENTS = {
    'github': {
        'client_id': 'b212c829c357ea0bd950',
        'client_secret': 'e2bdda59f9da853ec39d0d1e07baade595f50202',
    }
}
PEEWEE_MIGRATIONS_PATH = 'example/migrations'
PEEWEE_CONNECTION = os.environ.get('DATABASE_URL', 'sqlite:///example.sqlite')

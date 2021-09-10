"""Default configuration options."""

from pathlib import Path


ROOT = Path(__file__).parent.parent

# Application options
STATIC_FOLDERS: str = [ROOT / 'assets']
STATIC_URL_PREFIX: str = '/assets'


# Muffin-Jinja options
JINJA2_TEMPLATE_FOLDERS: str = [ROOT / 'templates']

# Muffin-OAuth options
OAUTH_CLIENTS = {
    'github': {
        'client_id': 'b212c829c357ea0bd950',
        'client_secret': 'e2bdda59f9da853ec39d0d1e07baade595f50202',
        'scope': 'user:email',
    }
}

# Muffin-Peewee options
PEEWEE_MIGRATIONS_PATH = ROOT.parent / 'migrations'
PEEWEE_CONNECTION = f"aiosqlite:///{ROOT.parent / 'example.sqlite'}"

# Muffin-Session options
SESSION_SECRET_KEY = 'Example-Secret'
SESSION_AUTO_MANAGE = True

# Muffin-Admin options
ADMIN_LOGOUT_URL = '/logout'
ADMIN_CUSTOM_CSS_URL = '/assets/admin.css'
ADMIN_AUTH_STORAGE = 'cookies'
ADMIN_AUTH_STORAGE_NAME = 'session'

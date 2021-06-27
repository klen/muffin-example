"""Tests configuration options."""

# Import the project's settings
from .defaults import *     # noqa

# Application options
DEBUG = True

# Muffin-Peewee
PEEWEE_CONNECTION = 'sqlite+async:///:memory:'
PEEWEE_MANAGE_CONNECTIONS = False
PEEWEE_CONNECTION_PARAMS = {}

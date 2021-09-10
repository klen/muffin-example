"""Tests configuration options."""

# Import the project's settings
from .defaults import *     # noqa

# Application options
DEBUG = True

# Muffin-Peewee
PEEWEE_CONNECTION = 'aiosqlite:///:memory:'
PEEWEE_AUTO_CONNECTION = False
PEEWEE_CONNECTION_PARAMS = {}

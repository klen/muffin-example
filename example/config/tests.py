"""Tests configuration options."""

# Import the project's settings
from .defaults import *     # noqa

# Application options
DEBUG = True

# Muffin-Peewee
PEEWEE_CONNECTION = 'sqlite:///:memory:'
PEEWEE_CONNECTION_PARAMS = {}

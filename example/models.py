"""The application's models."""

import datetime as dt

import hmac
import random
import peewee as pw
import hashlib

from . import db


@db.register
class Test(db.Model):
    """A simple model."""

    data = pw.CharField()


@db.register
class User(db.Model):
    """Implement application's users."""

    created = pw.DateTimeField(default=dt.datetime.now)
    username = pw.CharField()
    email = pw.CharField(unique=True)
    password = pw.CharField()
    is_super = pw.BooleanField(default=False)

    @classmethod
    def generate_password(cls, password, digestmod='sha256', salt_length=8):
        """Hash a password with given method and salt length."""
        salt = ''.join(random.sample('1234567890ABCDEFGabcdefg', salt_length))
        signature = create_signature(salt, password, digestmod=digestmod)
        return '$'.join((digestmod, salt, signature))

    def check_password(self, password):
        """Check the given password."""
        digestmod, salt, signature = self.password.split('$', 2)
        return hmac.compare_digest(
            signature, create_signature(salt, password, digestmod=digestmod))


@db.register
class Token(db.Model):
    """Store OAuth tokens."""

    provider = pw.CharField()
    token = pw.CharField()
    token_secret = pw.CharField(null=True)

    user = pw.ForeignKeyField(User)

    class Meta:
        """Tune the model."""

        indexes = (('token', 'provider'), True),


@db.register
class Message(db.Model):
    """Store user messages."""

    created = pw.DateTimeField(default=dt.datetime.utcnow)
    content = pw.CharField()
    user = pw.ForeignKeyField(User, null=True)


def create_signature(secret, value, digestmod='sha256', encoding='utf-8'):
    """Create HMAC Signature from secret for value."""
    if isinstance(secret, str):
        secret = secret.encode(encoding)

    if isinstance(value, str):
        value = value.encode(encoding)

    if isinstance(digestmod, str):
        digestmod = getattr(hashlib, digestmod, hashlib.sha1)

    hm = hmac.new(secret, digestmod=digestmod)
    hm.update(value)
    return hm.hexdigest()

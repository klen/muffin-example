import pytest
from mixer.backend.peewee import Mixer


@pytest.fixture(params=[
    pytest.param(('asyncio', {'use_uvloop': False}), id='asyncio'), 'trio',
], scope='session')
def aiolib(request):
    """Test the example with asyncio and trio."""
    return request.param


@pytest.fixture(autouse=True)
def db_trans(app):
    """Rollback DB after every test."""
    db = app.plugins['peewee']
    with db.atomic():
        yield db
        db.rollback()


@pytest.fixture(scope='session')
def mixer():
    return Mixer()


@pytest.fixture
def admin(mixer):
    """Generate an admin user."""
    admin = mixer.blend('example.models.User', email='admin@example.com', is_super=True)
    admin.password = admin.generate_password('pass')
    admin.save()
    return admin


@pytest.fixture
def user(mixer):
    """Generate an simple user."""
    user = mixer.blend('example.models.User', email='user@example.com')
    user.password = user.generate_password('pass')
    user.save()
    return user

import pytest
from mixer.backend.peewee import Mixer


@pytest.fixture(params=[
    pytest.param(('asyncio', {'use_uvloop': False}), id='asyncio'),
    #  'trio',
], scope='session')
def aiolib(request):
    """Test the example with asyncio and trio."""
    return request.param


@pytest.fixture(scope='session', autouse=True)
def setup_logging():
    import logging

    logger = logging.getLogger('peewee')
    logger.setLevel(logging.DEBUG)


@pytest.fixture(autouse=True, scope='session')
async def db(app):
    async with app.plugins['peewee'] as db:
        async with db.manager.connection(False):
            await db.create_tables()
            yield db


@pytest.fixture(autouse=True)
async def trans(app, db):
    """Rollback DB after every test."""
    db = app.plugins['peewee']
    async with db.transaction(silent=True) as trans:
        yield db
        await trans.rollback()


@pytest.fixture(scope='session')
def mixer():
    return Mixer(commit=False)


@pytest.fixture
async def admin(mixer):
    """Generate an admin user."""
    admin = mixer.blend('example.models.User', email='admin@example.com', is_super=True)
    admin.password = admin.generate_password('pass')
    return await admin.save(force_insert=True)


@pytest.fixture
async def user(mixer):
    """Generate an simple user."""
    user = mixer.blend('example.models.User', email='user@example.com')
    user.password = user.generate_password('pass')
    return await user.save(force_insert=True)

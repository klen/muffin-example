async def test_config(app):
    assert app.cfg.CONFIG == 'example.config.tests'


async def test_basic_views(app, client):
    response = await client.get('/')
    assert response.status_code == 200
    text = await response.text()
    assert "Hello anonimous!" in text

    response = await client.get('/404')
    assert response.status_code == 404

    response = await client.get('/json')
    json = await response.json()
    assert json
    assert json['json'] == 'here'


async def test_login_logout(client, user):
    response = await client.get('/')
    text = await response.text()
    assert "Hello anonimous!" in text

    response = await client.post('/login/', data={'email': user.email, 'password': 'pass'})
    assert response.status_code == 200
    text = await response.text()
    assert f"Hello {user.email}" in text

    response = await client.get('/logout')
    assert response.status_code == 200
    text = await response.text()
    assert "Hello anonimous" in text

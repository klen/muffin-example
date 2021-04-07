async def test_admin_auth(client, admin, user):
    res = await client.get('/admin', follow_redirect=False)
    assert res.status_code == 307

    # Login as an simple user
    res = await client.post('/login', data={'email': user.email, 'password': 'pass'})
    assert res.status_code == 200

    res = await client.get('/admin', follow_redirect=False)
    assert res.status_code == 307

    # Login as an admin
    res = await client.post('/login', data={'email': admin.email, 'password': 'pass'})
    assert res.status_code == 200

    res = await client.get('/admin', follow_redirect=False)
    assert res.status_code == 200
    assert 'initAdmin' in await res.text()

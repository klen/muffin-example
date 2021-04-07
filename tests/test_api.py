async def test_messages(client, mixer, user):
    res = await client.get('/api/messages')
    assert res.status_code == 200
    assert await res.json() == []

    mixer.cycle(3).blend('example.models.Message', user=user)
    res = await client.get('/api/messages')
    assert res.status_code == 200
    json = await res.json()
    assert json
    breakpoint()
    assert len(json) == 3

    res = await client.post('/api/messages', json={'content': 'example message'})
    assert res.status_code == 200
    json = await res.json()
    assert json['id']
    assert not json['user']

    await client.post('/login', data={'email': user.email, 'password': 'pass'})
    res = await client.post('/api/messages', json={'content': 'example message'})
    assert res.status_code == 200
    json = await res.json()
    assert json['id']
    assert json['user'] == str(user.id)



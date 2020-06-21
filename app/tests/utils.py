

def register(client, username, email, password):
    return client.post('/users/register', json={
        'username': username,
        'email': email,
        'password': password
    })

def login(client, email, password):
    return client.post('/users/login', json={
        'email': email,
        'password': password
    })

def logout(client, token=None):
    headers = None if not token else {'access-token': token}
    return client.post('/users/logout', headers=headers)

def authorize(client, token=None):
    headers = None if not token else {'access-token': token}
    return client.post('/users/authorize', headers=headers)

def get_user(client, id):
    return client.get('users/{}'.format(id))

def edit_user(client, id, body):
    return client.put('users/{}'.format(id), json=body)

def get_stats(client, date=None):
    query_string = {}
    if date != None:
        query_string['date'] = date
    return client.get('/stats', query_string=query_string)

def register(client, username=None, email=None, password=None):
    request = {}
    if username != None:
        request['username'] = username
    if email != None:
        request['email'] = email
    if password != None:
        request['password'] = password

    return client.post('/users/register', json=request)

def login(client, email, password):
    return client.post('/users/login', json={
        'email': email,
        'password': password
    })

def oauth2_login(client, email=None, photo=None):
    return client.post('/users/oauth2login', json={
        'email': email,
        'idToken': 1,
        'photoURL': photo
    })

def logout(client, token=None):
    headers = None if not token else {'access-token': token}
    return client.post('/users/logout', headers=headers)

def authorize(client, token=None):
    headers = None if not token else {'access-token': token}
    return client.post('/users/authorize', headers=headers)

def get_user(client, id):
    return client.get('/users/{}'.format(id))

def edit_user(client, id, body):
    return client.put('/users/{}'.format(id), json=body)

def get_users(client):
    return client.get('/users')

def delete_user(client, id):
    return client.delete('/users/{}'.format(id))

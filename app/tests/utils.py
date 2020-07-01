def get_stats(client, timestamp=None):
    query_string = {}
    if timestamp != None:
        query_string['timestamp'] = timestamp
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
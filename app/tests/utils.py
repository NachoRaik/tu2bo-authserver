TEST_API_KEY = 'asdf' 

def get_stats(client, initial_date=None, final_date=None):
    query_string = {}
    if initial_date != None:
        query_string['initial_date'] = initial_date
    if final_date != None:
        query_string['final_date'] = final_date
    return client.get('/stats', query_string=query_string)

def register(client, username=None, email=None, password=None):
    request = {}
    if username != None:
        request['username'] = username
    if email != None:
        request['email'] = email
    if password != None:
        request['password'] = password

    return client.post('/users/register', json=request, headers=headers_with_api_key())

def login(client, email, password):
    return client.post('/users/login', json={
        'email': email,
        'password': password
    }, headers=headers_with_api_key())

def oauth2_login(client, email=None, photo=None):
    return client.post('/users/oauth2login', json={
        'idToken': email,
        'photoURL': photo
    }, headers=headers_with_api_key())

def logout(client, token=None):
    headers = headers_with_api_key()
    if token: 
        headers['access-token'] = token
    return client.post('/users/logout', headers=headers)

def authorize(client, token=None):
    headers = headers_with_api_key()
    if token:
        headers['access-token'] = token
    return client.post('/users/authorize', headers=headers)

def get_user(client, id):
    return client.get('/users/{}'.format(id), headers=headers_with_api_key())

def edit_user(client, id, body):
    return client.put('/users/{}'.format(id), json=body, headers=headers_with_api_key())

def get_users(client):
    return client.get('/users', headers=headers_with_api_key())

def delete_user(client, id):
    return client.delete('/users/{}'.format(id), headers=headers_with_api_key())

def reset_password(client, email=None):
    body = {}
    if email: body['email'] = email
    return client.post('/users/reset_password', json=body, headers=headers_with_api_key())

def validate_reset_code(client, code, email):
    url = '/users/password?code={}&email={}'.format(code, email)
    return client.get(url, headers=headers_with_api_key())

def change_password(client, code, email, new_password):
    url = '/users/password?code={}&email={}'.format(code, email)
    return client.post(url, json={'password': new_password}, headers=headers_with_api_key())

def block_user(client, id):
    return client.post('/users/{}/blocked'.format(id), headers=headers_with_api_key())

def unblock_user(client, id):
    return client.delete('/users/{}/blocked'.format(id), headers=headers_with_api_key())

def headers_with_api_key():
    return { 'x-api-key': TEST_API_KEY }

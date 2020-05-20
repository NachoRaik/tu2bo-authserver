import pytest
from mongoengine import connect, disconnect
from mongoengine.connection import _get_db

class TestUsersController:
    def setup_method(self, method):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        connect('authserver-db-test', host='mongomock://localhost', alias='test')


    def teardown_method(self, method):
        """ teardown any state that was previously setup with a setup_method
        call.
        """
        db = _get_db()
        db.drop_collection('user')
        disconnect(alias='test')

    def test_register_success(self, client):
        """ POST /users/register
        Should: return 200 and correct message """

        res = client.post('/users/register', json={
            'username': 'oli',
            'email': 'olifer97@gmail.com',
            'password': '123'
        })
        json = res.get_json()
        assert json['id'] == 1
        assert res.status_code == 200

    def test_register_failure(self, client):
        """ POST /users/register with invalid email
        Should: return 400 and correct message """

        res = client.post('/users/register', json={
            'username': 'oli_wrong',
            'email': 'invalid_email',
            'password': '123'
        })
        assert b'Invalid email address' in res.data
        assert res.status_code == 400
    
    def test_login_success(self, client, register):
        """ POST /users/login
        Should: return 200 and correct message """

        res = client.post('/users/login', json={
            'email': 'olifer97@gmail.com',
            'password': '123'
        })
        json = res.get_json()
        assert 'token' in json
        assert res.status_code == 200

    def test_login_failure_password(self, client, register):
        """ POST /users/login wrong password
        Should: return 401 and correct message """

        res = client.post('/users/login', json={
            'email': 'olifer97@gmail.com',
            'password': '1234'
        })
        assert b'Password incorrect' in res.data
        assert res.status_code == 401

    def test_login_failure_inexistent(self, client):
        """ POST /users/login user does not exist
        Should: return 401 and correct message """

        res = client.post('/users/login', json={
            'email': 'olifer97@gmail.com',
            'password': '123'
        })
        assert b'Could not find user' in res.data
        assert res.status_code == 401

import pytest
from mongoengine import connect, disconnect

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
        disconnect(alias='test')

    def test_register_success(self, client):
        """ POST /users/register
        Should: return 200 and correct message """

        res = client.post('/users/register', json={
            'username': 'oli',
            'email': 'olifer97@gmail.com',
            'password': '123'
        })
        assert b'{"id":1}' in res.data
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

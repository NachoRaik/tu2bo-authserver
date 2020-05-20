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

    def test_register(self, client):
        """ POST /users/register
        Should: return 200 and correct message """

        res = client.post('/users/register', json={
            'username': 'oli',
            'email': 'olifer97@gmail.com',
            'password': '123'
        })
        assert b'{"id":1}' in res.data
        assert res.status_code == 200

import pytest
from mongoengine import connect, disconnect
from mongoengine.connection import _get_db
from database.models.user import User

class TestUsersController:
    def setup_method(self, method):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        connect('authserver-db-test', host='mongomock://localhost', alias='test_user')


    def teardown_method(self, method):
        """ teardown any state that was previously setup with a setup_method
        call.
        """
        db = _get_db()
        db.drop_collection('user')
        disconnect(alias='test_user')

    def test_create_user(self):
        """ Create user in db
        Should: return save user in db """

        user = User(username='oli', email="olifer97@gmail.com", password="123")
        user.save()

        fresh_user = User.objects().first()
        assert fresh_user.username ==  'oli'
        assert fresh_user.email ==  'olifer97@gmail.com'
        assert fresh_user.password ==  '123'

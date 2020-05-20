import pytest
import datetime as dt
import time
from mongoengine import connect, disconnect
from mongoengine.connection import _get_db
from database.models.invalid_token import InvalidToken

class TestInvalidToken:
    def setup_method(self, method):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        connect('authserver-db-test', host='mongomock://localhost', alias='test_invalid_token')


    def teardown_method(self, method):
        """ teardown any state that was previously setup with a setup_method
        call.
        """
        db = _get_db()
        db.drop_collection('invalid_token')
        disconnect(alias='test_invalid_token')

    def test_create_invalid_token(self):
        """ Create invalid token in db
        Should: return save invalid token in db """
        date = dt.datetime.utcnow()
        invalid_token = InvalidToken(token='token', expire_at=date)
        invalid_token.save()

        fresh_invalid_token = InvalidToken.objects().first()
        assert fresh_invalid_token.token ==  'token'

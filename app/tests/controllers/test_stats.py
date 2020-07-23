import pytest
import json
from mongoengine import connect, disconnect
from mongoengine.connection import _get_db
from tests.utils import *

class TestMonitoringController:
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
        db.drop_collection('user_stat')
        db.drop_collection('user')
        disconnect(alias='test')

    def test_stats_empty(self, client):
        """ GET /stats 
        Should: return 200 and stats"""

        res = get_stats(client, initial_date='06/29/20 18:03:31')
        assert res.status_code == 200

        body = json.loads(res.get_data())
        assert len(body) == 0

    def test_stats_with_one_user(self, client):
        """ GET /stats 
        Should: return 200 and stats"""

        res = register(client, 'user', 'test@mail.com', '123')
        assert res.status_code == 200

        res = get_stats(client, initial_date='06/29/20 18:03:31')
        body = json.loads(res.get_data())
        assert res.status_code == 200
        assert len(body) == 1
        assert body[0]['count'] == 1

    def test_stats_with_many_users(self, client):
        """ GET /stats 
        Should: return 200 and stats"""

        cant_users = 10
        for i in range(cant_users):
            res = register(client, 'user{}'.format(i), 'test{}@mail.com'.format(i), '123')
            assert res.status_code == 200
        res = get_stats(client, initial_date='06/29/20 18:03:31')
        body = json.loads(res.get_data())
        assert res.status_code == 200
        assert len(body) == cant_users
        for num_users in range(len(body)):
            assert body[num_users]['count'] == (num_users + 1)        

    def test_failed_registration_with_same_user(self, client):
        """ GET /stats 
        Should: return 200 and stats"""

        res = register(client, 'user', 'test@mail.com', '123')
        assert res.status_code == 200

        res = register(client, 'user', 'test@mail.com', '123')
        assert res.status_code == 409
        
        res = get_stats(client, initial_date='06/29/20 18:03:31')
        body = json.loads(res.get_data())
        assert res.status_code == 200
        assert len(body) == 1
        assert body[0]['count'] == 1

    def test_failed_registration_with_invalid_fields(self, client):
        """ GET /stats 
        Should: return 200 and stats"""

        res = register(client, username='user', email='test@mail.com')
        assert res.status_code == 400
        
        res = get_stats(client, initial_date='06/29/20 18:03:31')
        body = json.loads(res.get_data())
        assert res.status_code == 200
        assert len(body) == 0

    def test_stats_with_default_date(self, client):
        """ GET /stats 
        Should: return 200 and stats"""

        res = register(client, 'user', 'test@mail.com', '123')
        assert res.status_code == 200

        res = get_stats(client)
        body = json.loads(res.get_data())
        assert res.status_code == 200
        assert len(body) == 1
        assert body[0]['count'] == 1
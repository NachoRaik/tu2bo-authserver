import os
import tempfile
import pytest

from config import TestingConfig
from mongoengine import connect, disconnect
from app import create_app

@pytest.fixture
def client():
    """A test client for the app."""
    app = create_app(TestingConfig)
    return app.test_client()

@pytest.fixture
def context_register(client, scope='function'):
    """Register user."""
    res = client.post('/users/register', json={
        'username': 'oli',
        'email': 'olifer97@gmail.com',
        'password': '123'
    })
    return res.get_json()['id']

@pytest.fixture
def context_login(client, context_register, scope='function'):
    """Login user."""
    res = client.post('/users/login', json={
        'email': 'olifer97@gmail.com',
        'password': '123'
    })
    return res.get_json()['token']

@pytest.fixture
def context_logout(client, context_login, scope='function'):
    """Login user."""
    res = client.post('/users/logout', headers={
        'access-token': context_login
    })
    return context_login ##to know token logged out



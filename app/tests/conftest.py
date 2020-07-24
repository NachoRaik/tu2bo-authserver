import os
import tempfile
import pytest

from config import TestingConfig
from mongoengine import connect, disconnect
from app import create_app
from tests.utils import register, login, logout, block_user, oauth2_login
from flask_mail import Mail

@pytest.fixture
def app():
    """A test client for the app."""
    app = create_app(TestingConfig())
    return app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def mail(app):
    """Mailer for the app."""
    mail = Mail(app)
    return mail


@pytest.fixture
def context_register(client, scope='function'):
    """Register user."""
    res = register(client, 'oli', 'olifer97@gmail.com', '123')
    return res.get_json()['id']


@pytest.fixture
def context_oauth2login(client, scope='function'):
    """Register user by oauth."""
    res = oauth2_login(client, 'olifer97@gmail.com')
    return res.get_json()['user']['id']

@pytest.fixture
def context_login(client, context_register, scope='function'):
    """Login user."""
    res = login(client, 'olifer97@gmail.com','123')
    return res.get_json()['token']

@pytest.fixture
def context_logout(client, context_login, scope='function'):
    """Login user."""
    res = logout(client, context_login)
    return context_login ##to know token logged out

@pytest.fixture
def context_reset_password(client, context_register, scope='function'):
    """Reset password."""
    res = client.post('/users/reset_password', json={ 'email': 'olifer97@gmail.com'})
    return 1111 #code in testing


@pytest.fixture
def context_blocked(client, context_register, scope='function'):
    """Blocked user."""
    res = block_user(client, context_register)
    return context_register


import pytest
import json
from mongoengine import connect, disconnect
from mongoengine.connection import _get_db
from tests.utils import *

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
        db.drop_collection('invalid_token')
        db.drop_collection('reset_password_code')
        disconnect(alias='test')

    def test_register_success(self, client):
        """ POST /users/register
        Should: return 200 and with user id """

        res = register(client, 'oli', 'olifer97@gmail.com','123')
        body = json.loads(res.get_data())
        assert res.status_code == 200

    def test_register_failure_invalid_email(self, client):
        """ POST /users/register with invalid email
        Should: return 400 and correct message """

        res = register(client, 'oli_wrong', 'invalid_email','123')
        body = json.loads(res.get_data())
        assert res.status_code == 400
        assert 'Invalid email address' == body['reason']

    def test_register_failure_username_taken(self, client, context_register):
        """ POST /users/register with username taken
        Should: return 400 and correct message """

        res = register(client, 'oli', 'different@email.com','123') # same username as context
        body = json.loads(res.get_data())
        assert res.status_code == 409
        assert 'User already registered' == body['reason']

    def test_login_success(self, client, context_register):
        """ POST /users/login
        Should: return 200 and with token """

        res = login(client, 'olifer97@gmail.com','123')
        body = json.loads(res.get_data())
        assert 'token' in body
        assert body['user']['username'] == 'oli'
        assert body['user']['email'] == 'olifer97@gmail.com'
        assert res.status_code == 200

    def test_login_failure_password(self, client, context_register):
        """ POST /users/login wrong password
        Should: return 401 and correct message """

        res = login(client, 'olifer97@gmail.com','wrong')
        body = json.loads(res.get_data())
        assert res.status_code == 401
        assert 'Wrong credentials' == body['reason']

    def test_login_failure_inexistent(self, client): # without context_register
        """ POST /users/login user does not exist
        Should: return 401 and correct message """

        res = login(client, 'olifer97@gmail.com','123')
        body = json.loads(res.get_data())
        assert res.status_code == 401
        assert 'Wrong credentials' == body['reason']

    def test_authorize_success(self, client, context_login):
        """ POST /users/authorize
        Should: return 200 """

        res = authorize(client, context_login)
        user_info = json.loads(res.get_data())
        assert res.status_code == 200
        assert user_info['user']['username'] == 'oli'
        assert user_info['user']['email'] == 'olifer97@gmail.com'

    def test_authorize_failure_invalid(self, client):
        """ POST /users/authorize invalid token
        Should: return 401 """

        res = authorize(client, 'invalidtoken')
        body = json.loads(res.get_data())
        assert res.status_code == 401
        assert 'Invalid Token' == body['reason']

    def test_authorize_failure_logged_out(self, client, context_logout):
        """ POST /users/authorize token logged out
        Should: return 401 """

        res = authorize(client, context_logout)
        body = json.loads(res.get_data())
        assert res.status_code == 401
        assert 'Invalid Token' == body['reason']

    def test_authorize_failure_not_found(self, client):
        """ POST /users/authorize token not found
        Should: return 401 """

        res = authorize(client)
        body = json.loads(res.get_data())
        assert res.status_code == 401
        assert 'Token not found' == body['reason']

    def test_logout_success(self, client, context_login):
        """ POST /users/logout
        Should: return 205 """

        res = logout(client, context_login)
        assert res.status_code == 205

    def test_logout_failure(self, client):
        """ POST /users/logout No token
        Should: return 401 """

        res = logout(client)
        body = json.loads(res.get_data())
        assert res.status_code == 401

    def test_get_user_by_id_success(self, client, context_register):
        """ GET /users/id
        Should: return 200 with user data """

        res = get_user(client, context_register)
        user_info = json.loads(res.get_data())
        assert res.status_code == 200
        assert user_info['username'] == 'oli'
        assert user_info['email'] == 'olifer97@gmail.com'
        assert 'profile' in user_info
        assert 'picture' not in user_info['profile']

    def test_get_user_by_id_failure(self, client):
        """ GET /users/id
        Should: return 404 with correct message """

        res = get_user(client, 1)
        body = json.loads(res.get_data())
        assert res.status_code == 404
        assert 'Could not find user' == body['reason']

    def test_edit_user_profile_pic(self, client, context_register):
        """ GET /users/id
        Should: return 200 with updated user data """

        res =  edit_user(client, context_register, {'picture': 'someUrl.com/myImage'})
        user_info = json.loads(res.get_data())
        assert res.status_code == 200
        assert user_info['username'] == 'oli'
        assert user_info['email'] == 'olifer97@gmail.com'
        assert user_info['profile']['picture'] == 'someUrl.com/myImage'

        # checking if it is persisted
        res = get_user(client, context_register)
        user_info = json.loads(res.get_data())
        assert res.status_code == 200
        assert user_info['username'] == 'oli'
        assert user_info['email'] == 'olifer97@gmail.com'
        assert user_info['profile']['picture'] == 'someUrl.com/myImage'

    def test_edit_user_inexistent_field(self, client, context_register):
        """ GET /users/id
        Should: return 200 with same user data """

        res =  edit_user(client, context_register, {'myRandomField': 'blabla'})
        user_info = json.loads(res.get_data())
        assert res.status_code == 200
        assert user_info['username'] == 'oli'
        assert user_info['email'] == 'olifer97@gmail.com'
        assert 'myRandomField' not in user_info['profile']

    def test_get_users_success(self, client, context_register):
        """ GET /users/id
        Should: return 200 with user data """

        res = get_users(client)
        users = json.loads(res.get_data())
        assert res.status_code == 200
        assert len(users) == 1

    def test_reset_password_sends_email_success(self, client, mail, context_register):
        """ POST /users/reset_password
        Should: return 200 and send email """

        with mail.record_messages() as outbox:
            res = reset_password(client, 'olifer97@gmail.com')
            assert len(outbox) == 1
            assert outbox[0].subject == '[Tutubo] Restablecer contraseña'
            assert '1111' in outbox[0].body
            assert res.status_code == 200

    def test_reset_password_user_not_found(self, client, mail):
        """ POST /users/reset_password
        Should: return 200 and doesn't sends email """

        with mail.record_messages() as outbox:
            res = reset_password(client, 'olifer97@gmail.com')
            assert len(outbox) == 0
            assert res.status_code == 200

    def test_reset_password_missing_fields(self, client, mail):
        """ POST /users/reset_password
        Should: return 400 and doesn't sends email """

        with mail.record_messages() as outbox:
            res = reset_password(client)
            assert len(outbox) == 0
            assert res.status_code == 400

    def test_valid_reset_password_code(self, client, context_reset_password):
        """ GET /users/password?code=&email
        Should: return 200"""

        res = validate_reset_code(client, context_reset_password, 'olifer97@gmail.com')
        assert res.status_code == 200

    def test_invalid_reset_password_code(self, client):
        """ GET /users/password?code=&email
        Should: return 401"""

        res = validate_reset_code(client, 0000, 'olifer97@gmail.com')
        body = json.loads(res.get_data())
        assert res.status_code == 401
        assert 'Invalid code or email' == body['reason']

    def test_invalid_reset_password_email(self, client, context_reset_password):
        """ GET /users/password?code=&email
        Should: return 401"""

        res = validate_reset_code(client, context_reset_password, 'invalid@gmail.com')
        body = json.loads(res.get_data())
        assert res.status_code == 401
        assert 'Invalid code or email' == body['reason']

    def test_invalid_reset_password_provider(self, client, mail, context_oauth2login):
        """ POST /users/reset_password
        Should: return 200 and doesn't send mail"""

        with mail.record_messages() as outbox:
            res = client.post('/users/reset_password', json={'email': 'olifer97@gmail.com'})
            assert len(outbox) == 0
            assert res.status_code == 200

    def test_change_password_success(self,client, context_reset_password):
        """ POST /users/password?code=&email
        Should: return 204"""

        # newpassword is invalid
        res_login = login(client, 'olifer97@gmail.com','newpassword')
        assert res_login.status_code == 401

        # change password
        res = change_password(client, context_reset_password, 'olifer97@gmail.com', 'newpassword')
        assert res.status_code == 204

        # newpassword is valid
        res_login = login(client, 'olifer97@gmail.com','newpassword')
        assert res_login.status_code == 200

    def test_change_password_wrong_code_fails(self, client):
        """ POST /users/password?code=&email
        Should: return 401"""

        # newpassword is invalid
        res_login = login(client, 'olifer97@gmail.com','newpassword')
        assert res_login.status_code == 401

        # change password
        res = change_password(client, 0000, 'olifer97@gmail.com', 'newpassword')
        body = json.loads(res.get_data())
        assert res.status_code == 401
        assert 'Invalid code or email' == body['reason']

        # newpassword is still invalid
        res_login = login(client, 'olifer97@gmail.com','newpassword')
        assert res_login.status_code == 401

    def test_change_password_wrong_email_fails(self, client, context_reset_password):
        """ POST /users/password?code=&email
        Should: return 401"""

        # change password
        res = change_password(client, context_reset_password, 'invalid@gmail.com', 'newpassword')
        body = json.loads(res.get_data())
        assert res.status_code == 401
        assert 'Invalid code or email' == body['reason']

    def test_invalid_code_after_usage(self, client, context_reset_password):
        """ POST /users/password?code=&email
        Should: return 204"""

        # change password
        res = change_password(client, context_reset_password, 'olifer97@gmail.com', 'newpassword')
        assert res.status_code == 204

        # newpassword is valid
        res_login = login(client, 'olifer97@gmail.com','newpassword')
        assert res_login.status_code == 200

        # change password with same code
        res = change_password(client, context_reset_password, 'olifer97@gmail.com', 'newpassword')
        assert res.status_code == 401

    def test_delete_user_by_id_success(self, client, context_register):
        """ DELETE /users/id
        Should: return 200 """

        res = get_user(client, context_register)
        assert res.status_code == 200

        res = delete_user(client, context_register)
        assert res.status_code == 204

        res = get_user(client, context_register)
        assert res.status_code == 404

    def test_delete_user_by_id_failure(self, client): # no context_register
        """ DELETE /users/id
        Should: return 404 with correct message """

        res = delete_user(client, 100)
        body = json.loads(res.get_data())
        assert res.status_code == 404
        assert 'Could not find user' == body['reason']


    def test_register_oauth_success(self, client):
        """ POST /users/oauth2login
        Should: return 200 and with user id """

        res = oauth2_login(client, 'olifer97@gmail.com')
        body = json.loads(res.get_data())
        assert res.status_code == 200


    def test_register_oauth_verify_email(self, client):
        """ POST /users/oauth2login
        Should: return the email correctly """

        res = oauth2_login(client, 'olifer97@gmail.com')
        body = json.loads(res.get_data())
        assert body['user']['email'] == 'olifer97@gmail.com'

    def test_login_oauth_after_register(self, client):
        """ POST /users/oauth2login
        Should: return the same id, only generated once """

        #Register
        res = oauth2_login(client, 'olifer97@gmail.com')
        body = json.loads(res.get_data())
        generated_id = body['user']['id']

        #Login
        res = oauth2_login(client, 'olifer97@gmail.com')
        body = json.loads(res.get_data())
        assert body['user']['id'] == generated_id

    def test_block_user_by_id_success(self, client, context_register):
        """ POST /users/id/blocked
        Should: return 204 """

        res = login(client, 'olifer97@gmail.com','123')
        assert res.status_code == 200

        res = block_user(client, context_register)
        assert res.status_code == 204

        res = login(client, 'olifer97@gmail.com','123')
        body_blocked = json.loads(res.get_data())
        assert res.status_code == 401
        assert 'User is blocked' == body_blocked['reason']

    def test_block_user_by_id_success_unauthorize(self, client, context_login):
        """ POST /users/id/blocked
        Should: return 204 """

        res = authorize(client, context_login)
        body = json.loads(res.get_data())
        user_id = body['user']['id']
        assert res.status_code == 200

        res = block_user(client, user_id)
        assert res.status_code == 204

        res = authorize(client, context_login)
        body_blocked = json.loads(res.get_data())
        assert res.status_code == 401
        assert 'User is blocked' == body_blocked['reason']

    def test_block_user_by_id_failure(self, client): # no context_register
        """ POST /users/id/blocked
        Should: return 404 with correct message """

        res = block_user(client, 100)
        body = json.loads(res.get_data())
        assert res.status_code == 404
        assert 'Could not find user' == body['reason']

    def test_unblock_user_by_id_success(self, client, context_blocked):
        """ DELETE /users/id/blocked
        Should: return 204 """

        res = login(client, 'olifer97@gmail.com','123')
        body_blocked = json.loads(res.get_data())
        assert res.status_code == 401
        assert 'User is blocked' == body_blocked['reason']

        res = unblock_user(client, context_blocked)
        assert res.status_code == 204

        res = login(client, 'olifer97@gmail.com','123')
        assert res.status_code == 200

    def test_unblock_user_by_id_failure(self, client): # no context_register
        """ DELETE /users/id/blocked
        Should: return 404 with correct message """

        res = unblock_user(client, 100)
        body = json.loads(res.get_data())
        assert res.status_code == 404
        assert 'Could not find user' == body['reason']

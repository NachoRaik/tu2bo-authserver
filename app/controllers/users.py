import jwt
import datetime
from flask import Blueprint, request, jsonify, make_response
from flask import current_app as app
from flask_mail import Mail
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from collections import Counter
from controllers.utils import error_response, create_mail, get_reset_code
from middlewares.metrics import add_user_count

from mongoengine.errors import NotUniqueError, ValidationError
from database.models.user import User
from database.models.invalid_token import InvalidToken
from database.models.reset_password_code import ResetPasswordCode
from middlewares.metrics import add_user_count
from middlewares.security_wrapper import has_api_key

from google.oauth2 import id_token
from google.auth.transport import requests

HEADER_ACCESS_TOKEN = 'access-token'
REGISTER_FIELDS = ['email','password','username']
LOGIN_FIELDS = ['email','password']
RESET_PASSWORD_FIELDS = ['email']
NEW_PASSWORD_FIELDS = ['password']
OAUTH_FIELD = 'idToken'
ENCODING_ALGORITHM = 'HS256'


# -- Endpoints

def construct_blueprint(current_app):
    bp_users = Blueprint("bp_users", __name__, url_prefix="/users")

    mail = Mail(current_app)

    @bp_users.route('/register', methods=['POST'], strict_slashes=False)
    @has_api_key
    @add_user_count
    def register_user():
        body = request.get_json()
        if (not body or not Counter(REGISTER_FIELDS)==Counter(body.keys()) or len(body['password'])==0):
            app.logger.debug(" Registration || FAILURE || Bad Request --> %s %s", body, request.content_length, request.content_type)
            return error_response(400, 'Cant verify register')

        hashed_password = generate_password_hash(body['password'], method='sha256')
        try:
            user = User(email=body['email'],password=hashed_password,username=body['username'],provider="Tutubo").save()
            id = user.id
            response = jsonify({'id': id})
            response.status_code = 200
            return response
        except NotUniqueError:
            return error_response(409, 'User already registered')
        except ValidationError:
            return error_response(400, 'Invalid email address')

    @bp_users.route('/login', methods=['POST'], strict_slashes=False)
    @has_api_key
    def user_login():
        body = request.get_json()
        if (not body or not Counter(LOGIN_FIELDS)==Counter(body.keys())):
            return error_response(400, 'Cant verify email or password')

        try:
            user = User.objects.get(email=body['email'])
            if not check_password_hash(user.password,body['password']):
                return error_response(401, 'Wrong credentials')
            if user.is_blocked:
                return error_response(401, "User is blocked")
            token = jwt.encode({'email':user.email,'exp':datetime.datetime.utcnow() + datetime.timedelta(days=7)},app.config['SECRET_KEY'], algorithm=ENCODING_ALGORITHM)
            return jsonify({'token' : token.decode('UTF-8'), "user": user.serialize()})
        except User.DoesNotExist:
            return error_response(401, 'Wrong credentials')

    @bp_users.route('/oauth2login', methods=['POST'], strict_slashes=False)
    @has_api_key
    def user_oauth_login():
        body = request.get_json()
        if (not body or not OAUTH_FIELD in body.keys()):
            return error_response(400, 'Cant verify login credentials')

        try:
            idinfo = id_token.verify_oauth2_token(body['idToken'], requests.Request()) if not app.config['TESTING'] else {'email':body['idToken']}
            email = idinfo['email']
            user = User.objects(email=email)
            if not user:
                username = email.split('@')[0]
                username = "o_" + username
                photo = body['photoURL'] if 'photoURL' in body else None
                user = User(email=email, profile_pic=photo, username=username,provider="Google").save()
            else:
                user = user[0]
                if user.is_blocked:
                    return error_response(401, "User is blocked")

            token = jwt.encode({'email':user.email, 'exp':datetime.datetime.utcnow() + datetime.timedelta(days=7)}, app.config['SECRET_KEY'], algorithm=ENCODING_ALGORITHM)
            return jsonify({'token': token.decode('UTF-8'), "user": user.serialize()})
        except ValueError as err:
            return error_response(401, 'Cant verify Google credentials ' + str(err))

    @bp_users.route('/', methods=['GET'], strict_slashes=False)
    @has_api_key
    def get_users():
        users = jsonify(list(map(lambda user: user.serialize_admin(), User.objects())))
        users.status_code = 200
        return users

    @bp_users.route('/<userId>', methods=['GET', 'PUT', 'DELETE'])
    @has_api_key
    def user_profile(userId):
        user = User.objects.with_id(userId) #unique id
        if not user:
            return error_response(404, 'Could not find user')

        if request.method == 'PUT':
            body = request.get_json()
            user.profile_pic = user.profile_pic if not body or not 'picture' in body else body['picture']
            user.save()

        if request.method == 'DELETE':
            user.delete()
            return make_response("User deleted successfully", 204)

        user_profile = jsonify(user.serialize())
        user_profile.status_code = 200
        return user_profile


    @bp_users.route('/authorize', methods=['POST'])
    @has_api_key
    def user_authorize():
        if HEADER_ACCESS_TOKEN not in request.headers:
            return error_response(401, "Token not found")

        token = request.headers[HEADER_ACCESS_TOKEN]
        try:
            if len(InvalidToken.objects(token=token)) > 0:
                raise "Invalid Token" # token logged out

            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[ENCODING_ALGORITHM])
            user = User.objects.get(email=data['email'])
            if user.is_blocked:
                return error_response(401, "User is blocked")
            return jsonify({"user": user.serialize()})
        except:
            return error_response(401, "Invalid Token")


    @bp_users.route('/logout', methods=['POST'])
    @has_api_key
    def user_logout():
        if HEADER_ACCESS_TOKEN not in request.headers:
            return error_response(401, "Token not found")

        token = request.headers[HEADER_ACCESS_TOKEN]
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[ENCODING_ALGORITHM])
            expired_token = InvalidToken(token=token, expire_at=datetime.datetime.fromtimestamp(data['exp'])).save()
            return make_response("Logged out", 205)
        except:
            return make_response("Logged out", 205)

    @bp_users.route('/reset_password', methods=['POST'], strict_slashes=False)
    @has_api_key
    def user_reset_password():
        MSG = "Check your mail account for the reset code. Keep in mind non-existing and Google associated accounts cannot reset their passwords"
        body = request.get_json()
        if (not body or not Counter(RESET_PASSWORD_FIELDS)==Counter(body.keys())):
            return error_response(400, 'Missing fields')

        try:
            user = User.objects.get(email=body['email'],provider="Tutubo")
            code = get_reset_code(app.config['TESTING'])
            msg = create_mail(user.username, user.email, code)
            mail.send(msg)

            ResetPasswordCode(user_mail=body['email'], code=code, expire_at=datetime.datetime.utcnow() + app.config['RESET_CODE_TTL']).save()

            app.logger.debug("Reset password mail sent to %s",body['email'])
            return jsonify({'response' : MSG})
        except User.DoesNotExist:
            return jsonify({'response' : MSG})

    @bp_users.route('/password', methods=['GET','POST'], strict_slashes=False)
    @has_api_key
    def user_new_password():
        code = int(request.args.get('code'))
        email = request.args.get('email')
        try:
            reset_code = ResetPasswordCode.objects.get(user_mail=email, code=code)

            if request.method == 'GET':
                return make_response('Valid', 200)

            body = request.get_json()

            if (not body or not Counter(NEW_PASSWORD_FIELDS)==Counter(body.keys())):
                return error_response(400, 'Missing fields')

            hashed_password = generate_password_hash(body['password'], method='sha256')

            user = User.objects.get(email=email)
            user.password = hashed_password
            user.save()

            reset_code.delete()

            return make_response('Password changed', 204)

        except ResetPasswordCode.DoesNotExist:
            return error_response(401, 'Invalid code or email')

    @bp_users.route('/<userId>/blocked', methods=['POST', 'DELETE'], strict_slashes=False)
    @has_api_key
    def block_user(userId):
        user = User.objects.with_id(userId) #unique id
        if not user:
            return error_response(404, 'Could not find user')

        user.is_blocked = request.method == 'POST'
        user.save()
        response = 'User blocked' if request.method == 'POST' else 'User unblocked'
        return make_response(response, 204)

    return bp_users

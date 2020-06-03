from flask import Blueprint, request, jsonify, make_response
from flask import current_app as app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from collections import Counter
import jwt
import datetime

from mongoengine.errors import NotUniqueError, ValidationError
from database.models.user import User
from database.models.invalid_token import InvalidToken

HEADER_ACCESS_TOKEN = 'access-token'
REGISTER_FIELDS = ['email','password','username']
ENCODING_ALGORITHM = 'HS256'
LOGIN_FIELDS = ['email','password']
bp_users = Blueprint("bp_users", __name__, url_prefix="/users")

# -- Endpoints

@bp_users.route('/register', methods=['POST'], strict_slashes=False)
def register_user():
    body = request.get_json()
    if (not body or not     Counter(REGISTER_FIELDS)==Counter(body.keys())):
        return make_response('Cant verify register',400)
    hashed_password = generate_password_hash(body['password'], method='sha256')
    try:
        user = User(email=body['email'],password=hashed_password,username=body['username']).save()
        id = user.id
        response = jsonify({'id': id})
        response.status_code = 200
        return response
    except NotUniqueError:
        return make_response('User already registered', 409)
    except ValidationError:
        return make_response('Invalid email address', 400)

@bp_users.route('/login', methods=['POST'], strict_slashes=False)
def user_login():
    body = request.get_json()
    if (not body or not Counter(LOGIN_FIELDS)==Counter(body.keys())):
        return make_response('Cant verify email or password',400,{'auth':'login-required'})

    try:
        user = User.objects.get(email=body['email'])
        if not check_password_hash(user.password,body['password']):
            return make_response('Password incorrect',401)
        token = jwt.encode({'email':user.email,'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=24)},app.config['SECRET_KEY'], algorithm=ENCODING_ALGORITHM)
        return jsonify({'token' : token.decode('UTF-8'), "user": user.serialize()})
    except User.DoesNotExist:
        return make_response('Could not find user',401)

@bp_users.route('/', methods=['GET'], strict_slashes=False)
def get_users():
    users = jsonify(list(map(lambda user: user.serialize(), User.objects())))
    users.status_code = 200
    return users


@bp_users.route('/<userId>', methods=['GET'])
def get_user_profile(userId): # TODO: Paginate users
    try:
        user_profile = jsonify(User.objects(id=userId)[0].serialize()) #unique id
        user_profile.status_code = 200
        return user_profile
    except:
        return make_response('Could not find user',401)


@bp_users.route('/authorize', methods=['POST'])
def user_authorize():
    if HEADER_ACCESS_TOKEN not in request.headers:
        return make_response("Token not found",401,{'message':'Unauthorized'})
    token = request.headers[HEADER_ACCESS_TOKEN]
    try:
        if len(InvalidToken.objects(token=token)) > 0: 
            raise "Invalid Token" # token logged out

        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[ENCODING_ALGORITHM])
        user = User.objects.get(email=data['email'])
        return jsonify({"user": user.serialize()})
    except:
        return make_response("Invalid Token",401,{'message':'Unauthorized'})


@bp_users.route('/logout', methods=['POST'])
def user_logout():
    if HEADER_ACCESS_TOKEN not in request.headers:
        return make_response("Token not found",401,{'message':'Unauthorized'})
    token = request.headers[HEADER_ACCESS_TOKEN]
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[ENCODING_ALGORITHM])
        expired_token = InvalidToken(token=token, expire_at=datetime.datetime.fromtimestamp(data['exp'])).save()
        return make_response("Logged out",205)
    except:
        return make_response("Logged out",205)

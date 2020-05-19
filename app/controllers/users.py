from flask import Blueprint, request, jsonify, make_response
from flask import current_app as app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

from mongoengine.errors import NotUniqueError
from database.models.user import User
from database.models.token import Token

bp_users = Blueprint("bp_users", __name__, url_prefix="/users")

# -- Endpoints

@bp_users.route('/register', methods=['POST'], strict_slashes=False)
def register_user():
    body = request.get_json()
    hashed_password = generate_password_hash(body['password'], method='sha256')
    try:
        user = User(email=body['email'],password=hashed_password,username=body['username']).save()
        id = user.id
        response = jsonify({'id': id})
        response.status_code = 200
        return response
    except NotUniqueError:
        return make_response('User already registered', 400)

@bp_users.route('/login', methods=['POST'], strict_slashes=False)
def user_login():
    body = request.get_json()
    if (not body or not body.get('email') or not body.get('password')):
        return make_response('Cant verify email or password',400,{'auth':'login-required'})

    try:
        user = User.objects.get(email=body['email'])
        if not check_password_hash(user.password,body['password']):
            return make_response('Password incorrect',401)
        token = jwt.encode({'email':user.email,'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=24)},app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8'),'status':'OK'})
    except User.DoesNotExist:
        return make_response('Could not find user',401)

@bp_users.route('/', methods=['GET'], strict_slashes=False)
def get_users():
    users = jsonify(list(map(lambda user: user.serialize(), User.objects())))
    users.status_code = 200
    return users


@bp_users.route('/<userId>', methods=['GET'])
def get_user_profile(userId):
    user_profile = jsonify(User.objects(id=userId)[0].serialize()) #unique id
    user_profile.status_code = 200
    return user_profile


@bp_users.route('/auth', methods=['POST'])
def user_authorize():
    token = None
    if 'access-token' in request.headers:
        token = request.headers['access-token']
    if not token:
        return make_response("Token not found",401,{'message':'Unauthorized'})
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
        return make_response("Authorized",200, {'status':'OK','user': data['email']})
    except:
        return make_response("Invalid Token",401,{'message':'Unauthorized'})


@bp_users.route('/logout', methods=['POST'])
def user_logout():
    token = None
    if 'access-token' in request.headers:
        token = request.headers['access-token']
    if not token:
        return make_response("Token not found",401,{'message':'Unauthorized'})
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
        print(data)
        expired_token = Token(token=token, expire_at=datetime.datetime.utcnow() + datetime.timedelta(seconds=120)).save()
        return make_response("Authorized",200, {'status':'OK','user': data['email']})
    except jwt.exceptions.InvalidTokenError:
        return make_response("Invalid Token",401,{'message':'Unauthorized'})

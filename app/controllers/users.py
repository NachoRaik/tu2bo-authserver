from flask import Blueprint, request, jsonify, make_response
from flask import current_app as app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

from database.models.user import User

bp_users = Blueprint("bp_users", __name__, url_prefix="/users")

# -- Endpoints

@bp_users.route('/register', methods=['POST'], strict_slashes=False)
def register_user():
    body = request.get_json()
    hashed_password = generate_password_hash(body['password'], method='sha256')
    user = User(email=body['email'],password=hashed_password,name=body['name'],last_name=body['last_name']).save()
    id = user.id
    response = jsonify({'id': id})
    response.status_code = 200
    return response

@bp_users.route('/login', methods=['POST'], strict_slashes=False)
def user_login():
    body = request.get_json()
    if (not body or not body.get('email') or not body.get('password')):
        return make_response('Cant verify email or password',401,{'auth':'login-required'})

    try:
        user = User.objects.get(email=body['email'])
        if not check_password_hash(user.password,body['password']):
            return make_response('Password incorrect',401)
        token = token = jwt.encode({'email':user.email,'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=24)},app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8'),'status':'OK'})
    except User.DoesNotExist:
        return make_response('Could not find user',401)

from flask import Blueprint, request, jsonify, make_response
from flask import current_app as app
from werkzeug.utils import secure_filename
from database.models.user import User
import jwt
import datetime
from functools import wraps

bp_auth_users = Blueprint("bp_auth_users", __name__, url_prefix="/access")



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'access-token' in request.headers:
            token = request.headers['access-token']
        if not token:
            return make_response("Token not found",401,{'message':'Unauthorized'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user = user = User.objects.get(email=data['email'])
        except:
            return make_response("Invalid Token",401,{'message':'Unauthorized'})
        return f(user,*args, **kwargs)
    return decorated

# -- Endpoints

@bp_auth_users.route('/ping', methods=['GET'], strict_slashes=False)
@token_required
def access_ping(user):
    return make_response(user.email + " in Auth server is Authorized",200)

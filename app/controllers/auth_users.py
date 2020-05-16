from flask import Blueprint, request, jsonify
from flask import current_app as app
from werkzeug.utils import secure_filename

from database.models.user import User

bp_auth_users = Blueprint("bp_auth_users", __name__, url_prefix="/auth/users")

# -- Endpoints

@bp_auth_users.route('/', methods=['GET'], strict_slashes=False)
def get_users():
    users = jsonify(list(map(lambda user: user.serialize(), User.objects())))
    users.status_code = 200
    return users


@bp_auth_users.route('/', methods=['POST'], strict_slashes=False)
def add_users():
    body = request.get_json()
    user = User(**body).save()
    id = user.id
    response = jsonify({'id': id})
    response.status_code = 200
    return response


@bp_auth_users.route('/<userId>', methods=['GET'])
def get_user_profile(userId):
    user_profile = jsonify(User.objects(id=userId)[0].serialize()) #unique id
    user_profile.status_code = 200
    return user_profile

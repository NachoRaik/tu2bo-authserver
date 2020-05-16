from flask import Blueprint, request, jsonify
from flask import current_app as app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash


from database.models.user import User

bp_users = Blueprint("bp_users", __name__, url_prefix="/users")

# -- Endpoints


@bp_users.route('/register', methods=['POST'], strict_slashes=False)
def register_user():
    body = request.get_json()
    hashed_password = generate_password_hash(body['password'], method='sha256')
    user = User(email=body['email'],password=hashed_password,name=body['name'],last_name=body   ['last_name']).save()
    id = user.id
    response = jsonify({'id': id})
    response.status_code = 200
    return response

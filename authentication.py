from flask import Blueprint, request, jsonify
from flask import current_app as app
from werkzeug.utils import secure_filename
from config import firebaseConfig
from config import DevelopmentConfig
import pyrebase


bp_auth = Blueprint("bp_auth", __name__, url_prefix="/authentication")

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

@bp_auth.route('/register', methods=['POST'], strict_slashes=False)
def register():
    body = request.get_json()
    email=body["email"]
    password=body["password"]

    user = auth.create_user_with_email_and_password(email, password)
    auth.send_email_verification(user['idToken'])
    print("[INFO]: Success")
    response = jsonify({'status': 'OK'})
    response.status_code = 200
    return response


@bp_auth.route('/login', methods=['POST'], strict_slashes=False)
def login():
    body = request.get_json()
    email=body["email"]
    password=body["password"]

    login = auth.sign_in_with_email_and_password(email, password)
    print("[INFO]: Success")
    response = jsonify({'status': 'OK','token':login['idToken']})
    response.status_code = 200
    return response

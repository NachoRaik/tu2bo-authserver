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

HEADER_ACCESS_TOKEN = 'access-token'
REGISTER_FIELDS = ['email','password','username']
LOGIN_FIELDS = ['email','password']
RESET_PASSWORD_FIELDS = ['email']
NEW_PASSWORD_FIELDS = ['password']

ENCODING_ALGORITHM = 'HS256'


# -- Endpoints

def construct_blueprint(current_app):
    bp_users = Blueprint("bp_users", __name__, url_prefix="/users")
    
    mail = Mail(current_app)

    @bp_users.route('/register', methods=['POST'], strict_slashes=False)
    @add_user_count
    def register_user():
        body = request.get_json()
        if (not body or not Counter(REGISTER_FIELDS)==Counter(body.keys())):
            app.logger.debug(" Registration || FAILURE || Bad Request --> %s %s", body, request.content_length, request.content_type)
            return error_response(400, 'Cant verify register')
        
        hashed_password = generate_password_hash(body['password'], method='sha256')
        try:
            user = User(email=body['email'],password=hashed_password,username=body['username']).save()
            id = user.id
            response = jsonify({'id': id})
            response.status_code = 200
            return response
        except NotUniqueError:
            return error_response(409, 'User already registered')
        except ValidationError:
            return error_response(400, 'Invalid email address')

    @bp_users.route('/login', methods=['POST'], strict_slashes=False)
    def user_login():
        body = request.get_json()
        if (not body or not Counter(LOGIN_FIELDS)==Counter(body.keys())):
            return error_response(400, 'Cant verify email or password')

        try:
            user = User.objects.get(email=body['email'])
            if not check_password_hash(user.password,body['password']):
                return error_response(401, 'Wrong credentials')
            token = jwt.encode({'email':user.email,'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=24)},app.config['SECRET_KEY'], algorithm=ENCODING_ALGORITHM)
            return jsonify({'token' : token.decode('UTF-8'), "user": user.serialize()})
        except User.DoesNotExist:
            return error_response(401, 'Wrong credentials')

    @bp_users.route('/', methods=['GET'], strict_slashes=False)
    def get_users():
        users = jsonify(list(map(lambda user: user.serialize(), User.objects())))
        users.status_code = 200
        return users

    @bp_users.route('/<userId>', methods=['GET', 'PUT', 'DELETE'])
    def user_profile(userId): # TODO: Paginate users    
        user = User.objects.with_id(userId) #unique id
        if not user:
            return error_response(404, 'Could not find user')
        
        if request.method == 'PUT':
            body = request.get_json()
            user.profile_pic = user.profile_pic if not body or not 'picture' in body else body['picture']
            user.save()

        if request.method == 'DELETE':
            user.delete()
            return make_response("User deleted successfully", 200)

        user_profile = jsonify(user.serialize())
        user_profile.status_code = 200
        return user_profile


    @bp_users.route('/authorize', methods=['POST'])
    def user_authorize():
        if HEADER_ACCESS_TOKEN not in request.headers:
            return error_response(401, "Token not found")
        
        token = request.headers[HEADER_ACCESS_TOKEN]
        try:
            if len(InvalidToken.objects(token=token)) > 0: 
                raise "Invalid Token" # token logged out

            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[ENCODING_ALGORITHM])
            user = User.objects.get(email=data['email'])
            return jsonify({"user": user.serialize()})
        except:
            return error_response(401, "Invalid Token")


    @bp_users.route('/logout', methods=['POST'])
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
    def user_reset_password():
        body = request.get_json()
        if (not body or not Counter(RESET_PASSWORD_FIELDS)==Counter(body.keys())):
            return error_response(400, 'Missing fields')

        try:
            user = User.objects.get(email=body['email'])
            code = get_reset_code(app.config['TESTING'])
            msg = create_mail(user.username, user.email, code)
            mail.send(msg)

            ResetPasswordCode(user_mail=body['email'], code=code, expire_at=datetime.datetime.utcnow() + app.config['RESET_CODE_TTL']).save()

            app.logger.debug("Reset password mail sent to %s",body['email'])
            return jsonify({'response' : 'Email sent'})
        except User.DoesNotExist:
            return jsonify({'response' : 'Email sent'})

    @bp_users.route('/password', methods=['GET','POST'], strict_slashes=False)
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
    
    return bp_users


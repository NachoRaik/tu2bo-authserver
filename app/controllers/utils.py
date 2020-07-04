import json
from flask import Response
from flask_mail import Message

def error_response(code, msg):
    body = json.dumps({ 'reason':msg })
    return Response(body, status=code, mimetype='application/json')

def get_reset_code():
    return random.randint(1000,9999)

def create_mail(username, email):
    msg = Message('[Tutubo] Restablecer contraseña', sender='tutubo.applicacion@gmail.com', reply_to="noreply@tutubo.com", recipients = [email])
    code = get_reset_code()
    msg.body = "Código: {}".format(code)
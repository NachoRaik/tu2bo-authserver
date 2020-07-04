import json
from flask import Response
from flask_mail import Message
import random

def error_response(code, msg):
    body = json.dumps({ 'reason':msg })
    return Response(body, status=code, mimetype='application/json')

def get_reset_code(testing):
    return 1111 if testing else random.randint(1000,9999)

def create_mail(username, email, code):
    msg = Message('[Tutubo] Restablecer contraseña', sender='tutubo.applicacion@gmail.com', reply_to="noreply@tutubo.com", recipients = [email])
    msg.body = "Código: {}".format(code)
    return msg
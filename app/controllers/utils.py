import json
from flask import Response

def error_response(code, msg):
    return Response(json.dumps({ 'reason':msg }), status=code)
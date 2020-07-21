from flask import Response, request
from flask import current_app as app
from functools import wraps
import json

HEADER_API_KEY = 'x-api-key'

def has_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if HEADER_API_KEY not in request.headers or request.headers[HEADER_API_KEY] != app.config['MASTER_API_KEY']:
            app.logger.debug("/has_api_key || Invalid or not present API Key")
            return Response(json.dumps({ 'reason': 'API Key not found' }), status=401, mimetype='application/json')
        return f(*args, **kwargs)
    
    return decorated

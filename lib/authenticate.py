from functools import wraps
from flask import request, jsonify
from models.auth_token import AuthToken


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            auth_token = AuthToken.query.filter_by(auth_token=token).first()
            if not auth_token:
                return jsonify({'message': 'Token is invalid!'}), 403
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

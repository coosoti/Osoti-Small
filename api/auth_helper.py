"""Methods to generate auth tokens
"""

from flask import current_app
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
    )

def get_token(user_id, expires_in=1800, key=None):
    """ This function generates token helper """
    if key is None:
        key = current_app.config['SECRET_KEY']
    token = Serializer(key, expires_in)
    token_with_id = token.dumps({'id': user_id})
    return token_with_id.decode('ascii')

def token_id(token):
    """ This function check if the token is valid and returns id appended to it"""
    deserialize_token = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = deserialize_token.loads(token)
    except SignatureExpired:
        return False
    except BadSignature:
        return False
    return data['id']
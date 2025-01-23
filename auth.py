import json
import os
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from flask import request, _request_ctx_stack, jsonify

# Environment variables for Auth0 configuration
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
API_IDENTIFIER = os.getenv('AUTH0_API_IDENTIFIER')
ALGORITHMS = ["RS256"]
API_AUDIENCE = os.getenv('AUTH0_API_AUDIENCE')
JWKS_URL = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise AuthError({'code': 'missing_header',
            'description': 'Authorization header is missing'
        }, 401)

    parts = auth_header.split()

    if len(parts) != 2:
        raise AuthError({
            'code': 'malformed_header',
            'description': 'Authorization header is malformed'
        }, 400)
    
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with Bearer'
        }, 401)

    return parts[1]

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'missing_permissions',
            'description': 'Permissions are not included in the token payload'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'insufficient_permissions',
            'description': f'Permission {permission} is not granted to the user'
        }, 403)

    return True

def verify_decode_jwt(token):
    #Decoding the token
    try:
        unverified_header = jwt.get_unverified_header(token)
    except Exception as e:
        raise AuthError({
            'code': 'invalid_header',
            'description': f"Invalid JWT token: {str(e)}"
        }, 401)
    
    if unverified_header is None or 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': "Authorization malformed. The token is missing the kid (key ID)"
        }, 401)

    kid = unverified_header['kid']

    #Fetching the the JWKS token
    try:
        response = urlopen(JWKS_URL)
        jwks = json.loads(response.read())
    except Exception as e:
        raise AuthError({
            'code': 'invalid_jwks',
            'description': f"Unable to fetch JWKS: {str(e)}"
        }, 500) 

    rsa_key = {}
    for key in jwks['keys']:
        if key['kid'] == kid:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
            break

    if not rsa_key:
        raise AuthError({
            'code': 'key_not_found',
            'description': "Unable to find appropriate key in JWKS"
        }, 404)

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            return payload
        
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': "Invalid claims in token"
            }, 403)
        except Exception as e:
            raise AuthError({
                'code': 'token_verification_failed',
                'description': f"Unable to verify token: {str(e)}"
        }, 401)

    return payload

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload=payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
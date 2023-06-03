from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError
from core.utils import auth

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        return auth(self, request)

    def authenticate_header(self, request):
        return 'Bearer'

    @classmethod
    def create_jwt(cls, user):
        # Create the JWT payload
        payload = {
            'user_identifier': user.username,
            'exp': int((datetime.now() + timedelta(weeks=999)).timestamp()),
            'iat': datetime.now().timestamp(),
        }

        # Encode the JWT with your secret key
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return jwt_token

    # @classmethod
    # def get_the_token_from_header(cls, token):
    #     token = token.replace('Bearer', '').replace(' ', '')  # clean the token
    #     return token

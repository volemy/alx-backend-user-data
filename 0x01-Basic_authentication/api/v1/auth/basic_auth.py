#!/usr/bin/env python3
"""
module for basic_auth
"""
import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    class for basic authentication/authorization
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:  # noqa E501
        """
        get base 64
        authorization header value
        """
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        substring = "Basic "
        if substring in authorization_header:
            return authorization_header[6:]
        else:
            return None

    def decode_base64_authorization_header(self, base_64_authorization_header: str) -> str:  # noqa E501
        """
        decode base 64
        authorization header
        """
        if not base_64_authorization_header:
            return None
        if not isinstance(base_64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base_64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except Exception as e:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):  # noqa E501
        """
        get user credential
        from basic authorization
        """
        if not decoded_base64_authorization_header:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None

        details = decoded_base64_authorization_header.split(':', 1)

        return details[0], details[1]

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):  # noqa E501
        """
        returns the user instance based on
        his/her email and password
        """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None

        try:
            list_users = User.search({'email': user_email})
        except Exception as e:
            return None
        if not list_users:
            return None
        user = list_users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        retrieve current user instance for a request
        """
        auth_header = self.authorization_header(request)
        b64header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(b64header)
        creds = self.extract_user_credentials(decoded_header)
        user = self.user_object_from_credentials(creds[0], creds[1])
        return user

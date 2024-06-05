#!/usr/bin/env python3
""" Auth.py module
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method for requiring authentication
        """
        if not path or not excluded_paths:
            return True

        normalized_path = path.rstrip('/')

        for excluded_path in excluded_paths:
            if normalized_path == excluded_path.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header method"""
        if not request:
            return None
        if "Authorization" not in request.headers:
            return None
        return (request.headers.get('Authorization'))

    def current_user(self, request=None) -> TypeVar('User'):
        """current user method"""
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from request
        """
        if not request:
            return None
        session_id = os.getenv('SESSION_NAME')
        return request.cookies.get(session_id)

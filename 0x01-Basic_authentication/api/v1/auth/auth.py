#!/usr/bin/env python3
""" module for auth.py
"""
from flask import request
from typing import List, TypeVar
import fnmatch


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
            # if normalized_path == excluded_path.rstrip('/'):
            if fnmatch.fnmatch(normalized_path, excluded_path.rstrip('/')):
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

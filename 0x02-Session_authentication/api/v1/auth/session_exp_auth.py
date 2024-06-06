#!/usr/bin/env python3
""" Module for session_auth_exp
"""
from api.v1.auth.session_auth import SessionAuth
from typing import Dict
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Session Expiration """

    def __init__(self):
        expire_seconds = int(getenv('SESSION_DURATION', 0))
        self.session_duration = expire_seconds

    def create_session(self, user_id=None):
        """
            Make a new Session and register in the class with time
            Args:
                user_id: Identificator of the user_id
            Return:
                Session ID
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        session_dict: Dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
            Make a user ID based with time expiration
            Args:
                session_id: String of the session
            Return:
                User ID if not is expired
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        user_id = session_dict.get('user_id')
        if user_id is None:
            return None

        if self.session_duration <= 0:
            return user_id

        created_by = session_dict.get('created_at')
        if created_by is None:
            return None

        expired_session = created_by + timedelta(seconds=self.session_duration)
        if expired_session < datetime.now():
            return None

        return user_id

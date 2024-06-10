#!/usr/bin/env python3
"""
module for auth.py
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """
    takes in password string
    Returns:
        bytes
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    return a string uuid
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register a user
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {user.email} already exists")
        except NoResultFound:
            hsh_pass = _hash_password(password)
            new_user = self._db.add_user(email=email, hashed_password=hsh_pass)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        validate login
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = user.hashed_password
            if user:
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    return True
                else:
                    return False
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        create a session
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        get user from session id
        """
        if session_id:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                return None
        else:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        destroys a session
        """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        generate password reset token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return user.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        update password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hsh_pass = _hash_password(password)
            self._db.update_user(
                user.id, hashed_password=hsh_pass, reset_token=None)
            return None
        except NoResultFound:
            raise ValueError

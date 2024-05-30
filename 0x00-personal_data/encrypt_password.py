#!/usr/bin/env python3
"""
password encryption.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Arguments:
        password: a string representing the password to hash

    Returns:
        a salted, hashed password, which is a byte string
    """
    pswd_encoded = password.encode()
    pswd_hashed = bcrypt.hashpw(pswd_encoded, bcrypt.gensalt())
    return pswd_hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''Check valid password'''
    valid = False
    pswd_encoded = password.encode()
    if bcrypt.checkpw(pswd_encoded, hashed_password):
        valid = True
    return valid

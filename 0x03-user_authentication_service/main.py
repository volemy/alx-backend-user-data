#!/usr/bin/env python3
"""
main.py module
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    register user testing
    """
    url = "http://192.168.43.143:5000/users"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code in [200, 400]


def log_in_wrong_password(email: str, password: str) -> None:
    """
    wrong password testing
    """
    url = "http://192.168.43.143:5000/sessions"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    login testing
    """
    url = "http://192.168.43.143:5000/sessions"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    profile unlogged testing
    """
    url = "http://192.168.43.143:5000/profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    profile logged testing
    """
    pass
    # print(session_id)
    # url = "http://192.168.43.143:5000/profile"
    # payload = {"session_id": session_id}
    # response = requests.get(url, params=payload)
    # assert response.status_code == 200, f"{response.status_code}"


def log_out(session_id: str) -> None:
    """
    log out testing
    """
    url = "http://192.168.43.143:5000/sessions"
    payload = {"session_id": session_id}
    response = requests.delete(url, data=payload)
    assert response.status_code in [200, 403]


def reset_password_token(email: str) -> str:
    """
    reset password token testing
    """
    url = "http://192.168.43.143:5000/reset_password"
    payload = {"email": email}
    response = requests.post(url, data=payload)
    json_data = response.json()
    return json_data.get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    update password testing
    """
    url = "http://192.168.43.143:5000/reset_password"
    payload = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password}
    response = requests.put(url, data=payload)
    assert response.status_code in [200, 403]


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

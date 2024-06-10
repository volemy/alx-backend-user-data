#!/usr/bin/env python3
"""
module app.py
"""
from flask import Flask, jsonify, request, abort
from flask import make_response, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def index():
    """
    index route
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """
    list of users route
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login():
    """
    login method
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response_payload = {
            "email": email,
            "message": "logged in"
        }
        response = jsonify(response_payload)
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=['DELETE'])
def logout():
    """
    logout method
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
        else:
            abort(403)
    else:
        abort(403)


@app.route("/profile", methods=['GET'])
def profile():
    """
    get profile of user
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email})
    abort(403)


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token():
    """
    get reset password token
    """
    email = request.form.get('email')
    if email:
        try:
            reset_token = AUTH.get_reset_password_token(email)
            return jsonify({"email": email, "reset_token": reset_token})
        except ValueError:
            abort(403)
    abort(403)


@app.route("/reset_password", methods=['PUT'])
def update_password():
    """
    update password endpoint
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        if not AUTH.update_password(reset_token, new_password):
            return jsonify({
                "email": email,
                "message": "Password updated"}), 200
        else:
            abort(403)
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

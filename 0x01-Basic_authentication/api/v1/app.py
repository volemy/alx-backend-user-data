#!/usr/bin/env python3
"""
module for app.py
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
import importlib


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth = os.getenv('AUTH_TYPE')
if auth:
    auth_module = importlib.import_module(f'api.v1.auth.{auth}')
    if auth == 'auth':
        Auth = getattr(auth_module, 'Auth')
        auth = Auth()
    elif auth == 'basic_auth':
        BasicAuth = getattr(auth_module, 'BasicAuth')
        auth = BasicAuth()
else:
    auth_module = importlib.import_module(f'api.v1.auth.auth')
    Auth = getattr(auth_module, 'Auth')
    auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_access(error) -> str:
    """Unauthorized Access handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_status(error) -> str:
    """Forbidden Access handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def auth_before_request():
    """handles before request"""
    if not auth:
        pass

    epaths = ['/api/v1/stat*', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if auth.require_auth(request.path, epaths) is True:
        if auth.authorization_header(request) is None:
            abort(401)
        if auth.current_user(request) is None:
            abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

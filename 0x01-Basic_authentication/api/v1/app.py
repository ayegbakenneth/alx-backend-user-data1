#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
if ken_env_var == "RIGHT_AUTH_TYPE":
    auth = RightAuthType()
elif not_ken_env_var == "DIFFERENT_AUTH_TYPE":
    auth = DifferentAuthType

if auth:
    from api.v1.auth.auth import Auth
auth_instance = Auth()
auth = auth_instance


@app.before_request
def before_request():
    """ A method to handle the before_request """
    if auth is None:
        return


not_included = [
        '/api/v1/status/', '/api/v1/unauthorized/',
        '/api/v1/forbidden/']
if request.path not in not_included and auth.require_auth(
        request.path, not_included):
    return
if auth.authorization_header(request) is None:
    abort(401)
if auth.current_user(request) is None:
    abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ A not found error method """
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ An unauthorized method handler """
    return jsonify({"error": "unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ A forbidden error method """
    return jsonify({"error": "Forbidden"})


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

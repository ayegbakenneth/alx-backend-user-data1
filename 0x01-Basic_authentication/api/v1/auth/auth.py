#!/usr/bin/env python3
""" File executable path """

from flask import request
from typing import List, TypeVar
""" Module importation path """


class Auth:
    """ A  class to manage the API
    authentication."""

    def require_auth(
            self, path: str, excluded_paths: List[str]) -> bool:
        """ A method that require the auth path """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        path = path if path.endswith("/") else path + "/"

        for excluded_path in excluded_paths:
            excluded_path = excluded_path if excluded_path.endswith(
                    "/") else excluded_path + "/"
            if path.startswith(excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ This access the auth header """
        if request is None or request not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ This method access current_user """
        return None

#!/usr/bin/env python3
""" File executable path """

import bcrypt
""" Module importation path """


def hash_password(password):
    """ A function that returns
    a hashed password """
    pass_word = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pass_word, salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """  function that expects 2 
    arguments and returns a boolean """
    pass_word = password.encode('utf-8')
    return bcrypt.checkpw(pass_word, hashed_password)

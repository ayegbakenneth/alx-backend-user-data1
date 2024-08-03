#!/usr/bin/env python3
""" File executable path """
import os
import mysql.connector
import logging
import re
""" Module importation path """

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields, redaction, message, separator):
    """ filter_datum that returns the log message obfuscated """
    return re.sub(
        '|'.join(f'{field}=[^{separator}]*' for field in fields),
        lambda match: f'{match.group(0).split("=")[0]}={redaction}',
        message
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ method to filter values in incoming log records """
        return filter_datum(
                self.fields, self.REDACTION, super().format(
                    record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """  function that takes no arguments
    and returns a logging.Logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


def get_db():
    """Retrieve database credentials from environment variables"""
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    driver = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )

    return driver


def main():
    """ function that takes no arguments and returns nothing. """
    connector_db = get_db()
    cursor = connector_db.cursor()
    ken = cursor.execute("SELECT * FROM users")
    
    for row in ken:
        result = ken[row].filter_datum()
    return result


if __name__ == ('__main__'):
    main()

#!/usr/bin/env python3

from enum import Enum

"""
HELPER CLASSES
"""


class StatusCode(Enum):
    """Represents different HTTP Status Codes"""

    SUCCESS = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


class Response:
    """
    **A Response object to encapsulate information related to DB connection**
    connected: a bool indicating if the connection is established
    message: a string providing context of the Response
    connection: connection to the database
    status_code: an int indicating the HTTP status code
    """

    def __init__(self, connected=False, message="", connection=None, status_code=-1):
        self.connected = connected
        self.message = message
        self.connection = connection
        self.status_code = status_code

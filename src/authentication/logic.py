#!/usr/bin/env python3

import hashlib
import json

import mysql.connector
import pycountry
import yaml
from fastapi import HTTPException

from db_setup import close_connection, create_connection
from utilities.classes import Response, StatusCode

"""
HELPER FUNCTIONS
"""


def check_country_code(code: str) -> bool:
    """Function to check if the username meets the 2-letter country code criteria"""
    # invalid code
    if not code.isalpha():
        return False
    # non-existent country code
    elif pycountry.countries.get(alpha_2=code) == None:
        return False
    return True


def verify_credentials(username: str, password: str, config_file: str) -> Response:
    """Function to verify the username and password against the database"""
    config: object = read_yaml_config(config_file)

    try:
        # Retrieve data from config file
        host, port, db_name, db_user, db_password = (
            config["app"]["host"],
            config["app"]["port"],
            config["app"]["name"],
            config["app"]["user"],
            config["app"]["password"],
        )

        # Connect to DB
        response, cursor = create_connection(
            host, port, db_name, db_user, db_password)
        if not response.connected:
            response.message = "Error when connecting to DB"
            response.status_code = StatusCode.INTERNAL_SERVER_ERROR.value
            return response

        # Check if username & password exists in DB
        # case-insensitive search
        modifiedName: str = username[:2].lower() + username[2:]
        query: str = f"SELECT * FROM users WHERE username = '{modifiedName}'"
        cursor.execute(query)
        row = cursor.fetchone()

        if row:
            db_user, db_password = row[1], row[2]
            encrypted_password = hashlib.sha256(
                password.encode("utf-8")).hexdigest()
            if db_password == encrypted_password:
                response.message = f"Authentication successful for {db_user}"
                response.status_code = StatusCode.SUCCESS.value
            else:
                response.message = "Invalid password, try again"
                response.status_code = StatusCode.UNAUTHORIZED.value
        else:
            response.message = "Invalid name and/or password, try again"
            response.status_code = StatusCode.UNAUTHORIZED.value

        # TODO: when does a closure of DB connection happen on an actual app?
        # when user session ends?

    except mysql.connector.Error as e:
        response.message = e
        response.status_code = StatusCode.INTERNAL_SERVER_ERROR.value

    return response


def read_yaml_config(file_path) -> object:
    """Function to read YAML config file"""
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

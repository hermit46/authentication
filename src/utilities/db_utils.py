#!/usr/bin/env python3

import json

import mysql.connector

from authentication.db_setup import close_connection, create_connection
from authentication.logic import read_yaml_config
from utilities.classes import Response, StatusCode
from constants.constants import CONFIG_FILE, JSON_FILE_PATH
from typing import Optional

# ----------------------------------------------------------------
# create_table(connection) -> Response
# populate_user_table(response, cursor, json_file_path) -> Response
# create_connection(host, port, db_name, username, password) -> Response, cursor
# close_connection(connection) -> Response
# ----------------------------------------------------------------


def create_table(connection) -> Response:
    """
    Overview: Create the 'users' table in the database.

    Arguments:
    ------------
    A SQL Connection

    Returns:
    ------------
    A Response object


    """
    create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        )
    """
    try:
        # TODO: the logic here is faulty.
        # close_connection mutates the response object, but mutation doesn't persist
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        response.connected = True
        response.message = "Table 'users' created successfully."
        response.status_code = StatusCode.SUCCESS.value
        cursor.close()
        close_connection(connection)
    except mysql.connector.Error as e:
        response.message = f"Error creating the table: {e}"
    return response


def populate_user_table(response, cursor, json_file_path: str) -> Response:
    """Populates the user table with data from a given json file"""
    try:
        # TODO: think about the logic: a lot of duplicated code
        # when we keep re-establishing connection to DB

        with open(json_file_path, "r") as file:
            data = json.load(file)
            users = data["users"]

        insert_query = """
            INSERT INTO users (username, password_hash)
            VALUES (%s, %s)
        """

        for user in users:
            username = user["username"]
            password_hash = user["password_hash"]
            values = (username, password_hash)
            cursor.execute(insert_query, values)

        response.connection.commit()
        print("Data populated into 'user' table successfully.")
        cursor.close()
        close_connection(response.connection)
    except mysql.connector.Error as e:
        response.status_code = StatusCode.INTERNAL_SERVER_ERROR.value
        response.message = e
    return response


def create_connection(
    host, port, database_name, username, password
) -> Optional(Response, mysql.connector.cursor.MySQLCursor):
    """Create a database connection to the MySQL database."""
    response = Response()
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            database=database_name,
            user=username,
            password=password,
        )
        response.connected = True
        response.message = "Connection to MySQL database successful."
        response.connection = connection
        response.status_code = StatusCode.SUCCESS.value
        cursor = response.connection.cursor()
    except mysql.connector.Error as e:
        response.status_code = StatusCode.INTERNAL_SERVER_ERROR.value
        response.message = f"Error connecting to the database: {e}"
        cursor = None
    return response, cursor


def close_connection(connection) -> Response:
    """Close the database connection."""
    response = Response()
    try:
        if connection:
            connection.close()
            response.connected = False
            response.connection = None
            # response.message = "Connection closed."
            response.status_code = StatusCode.SUCCESS.value
    except mysql.connector.Error as e:
        response.status_code = StatusCode.INTERNAL_SERVER_ERROR.value
        response.message = f"Error closing the connection: {e}"
    return response


config = read_yaml_config(CONFIG_FILE)
host, port, db_name, db_user, db_password = (
    config["app"]["host"],
    config["app"]["port"],
    config["app"]["name"],
    config["app"]["user"],
    config["app"]["password"],
)

response, cursor = create_connection(host, port, db_name, db_user, db_password)

# table_creation = create_table(response.connection)
# print("Create Tabled: ", table_creation.status_code, table_creation.message)
# table_population = populate_user_table(response, cursor, JSON_FILE_PATH)
# print("Populate table: ", table_population.status_code, table_population.message)

import mysql.connector
from utils import Response, StatusCode


def create_connection(host, port, database_name, username, password) -> (Response, mysql.connector.cursor.MySQLCursor):
    """Create a database connection to the SQLite database."""
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

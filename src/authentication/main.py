#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError, constr

from utilities.utilities import check_country_code, verify_credentials
from utilities.classes import StatusCode
from constants.constants import CONFIG_FILE

app = FastAPI()


class UserCredentials(BaseModel):
    username: constr(min_length=3)
    password: constr(min_length=1)


"""
API Endpoints
"""


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/authenticate")
def login(credentials: UserCredentials):
    """
    Authenticate a user against a MySQL database.

    Args: credentials (UserCredentials): The user's login credentials

    Returns:
    JSON response:
        - 200 OK: Authentication successful.
        - 400 Bad Request: Invalid username or password format or invalid country code criteria.
        - 401 Unauthorized: Invalid username or password.

    Raises:
        HTTPException 400: If the username or password format, or country code format is invalid.
        HTTPException 401: If the username or password is incorrect.
    """
    try:
        countryCode = credentials.username[:2].lower()

        # Check if the username meets the 2-letter country code criteria
        if not check_country_code(countryCode):
            return HTTPException(
                status_code=StatusCode.BAD_REQUEST.value,
                detail="Username does not meet country code criteria",
            )

        response = verify_credentials(
            credentials.username, credentials.password, CONFIG_FILE
        )

        # DB Connection Unsuccessful
        if not response.connected:
            return HTTPException(
                status_code=response.status_code, detail=response.message
            )

        match response.status_code:
            case StatusCode.SUCCESS.value:
                return {
                    "success": response.connected,
                    "message": response.message,
                    "status_code": response.status_code,
                }
            case StatusCode.UNAUTHORIZED.value:
                return HTTPException(
                    status_code=response.status_code, detail=response.message
                )
            case StatusCode.INTERNAL_SERVER_ERROR.value:
                return HTTPException(
                    status_code=response.status_code, detail=response.message
                )

    # note that this doesn't run, because it's caught by constr (BaseModel)
    except ValidationError as ve:
        raise HTTPException(
            status_code=StatusCode.BAD_REQUEST.value, detail=ve.errors()
        )

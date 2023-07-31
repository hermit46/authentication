# Overview

An Authentication API that currently runs with FastAPI, verifies a provided UserCredential with a MySQL DB, and returns an appropriate response.

To do next:

- Include a monitoring dashboard for responses from API
- To handle virtual environment, consider:
  - containerization (Docker),
  - App deployment (Heroku),
  - Container orchestration (Kubernetes),
  - venv activation scripts
  - package managers (pipenv / poetry)

## Relevant commands

To activate virtual environment:
`source myenv/bin/activate`

To download all dependencies:
`pip3 install -r requirements.txt`

To run FASTAPI:
`uvicorn main:app --reload`

To update list of dependencies:
`pip3 freeze > requirements.txt`

## Backend Components:

1. API: FastAPI Python
2. DB: FreeDB (1 DB, 50MB, Limited Queries[^1])
3. Monitoring: Grafana (TODO)

[^1]: MAX QUERIES PER HOUR 800, MAX UPDATES PER HOUR 800, MAX_CONNECTIONS_PER_HOUR 800, MAX Connections 800

## API Logic:

1. First check if username and password provided meet minimum length requirements
2. Parse the country code out of the username and check if the country code is valid
3. Open database/file
4. Verify credentials against DB/file by checking for username match first, followed by match against hashed password input.
5. Return an appropriate message or error, depending on where in the authentication the input fails

## How to test the API:

1. First run uvicorn main:app --reload
2. Go to localhost:8000/docs to send POST requests

## Assumptions:

1. Usernames must be at least 3 characters long (2 for the country code, 1 for the name)
2. Passwords are at least 1 character long (made with extensibility in mind)
3. Passwords can include special characters like ! and numbers
4. pycountry's library contains a reliable source of alpha-2 country codes, which is used for authentication
5. User may input capital letters for country code, API is modified to still work
6. Country code in database is always lowercase

## Equivalence classes of test cases

Tested manually.

1. Valid username and password
2. Non-matched username, valid password
3. Valid username, invalid password
4. Invalid country code
5. Username too short, password too short

<!-- Personal Notes -->

<!-- Reasons for returning HTTP responses for db_setup:

1. Proper communication with clients deems that HTTP responses are a standard means to convey information
2. Status codes are useful for specificity, especially in cases of failure
3. Error handling can be done more gracefully to allow clients to troubleshoot
4. Structured Data (JSON, XML) from HTTP responses allows clients to parse data easily. Can also give plaintext
5. Standard web dev practices and consistency -->

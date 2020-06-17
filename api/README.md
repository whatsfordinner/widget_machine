# Widgets API

## Getting Started

This application uses `pipenv` for virtual environment and dependency management. The application itself is written in Python 3.8

1. Create new virutal environment and install dependencies with `pipenv install`  
2. Bring up the local development test scaffold `docker-compose -f docker-compose.local.yml up -d`  
3. Enter a virtual environment shell `pipenv shell`
4. Export Flask variables `export FLASK_ENV=development` and `export FLASK_APP=api`  
5. Run the API `flask run`

## Structure

The application uses the Flask application factory pattern. The `api` package builds the Flask application and builds the callable WSGI object. The two resources are contained within their own sub-packages and use the following setup:

* the `routes` module defines the endpoints and methods supported by the package and provides the blueprint to be used by the Flask app  
* the `handlers` module contains the business logic for the API  
* the `utils` module contains helper functions and objects (E.g. JSON schema validators)  
* the `exceptions` module contains all the exceptions used within the package  
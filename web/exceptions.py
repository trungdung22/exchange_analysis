# -*- coding: utf-8 -*-


class InternalServerError(Exception):
    pass


class InvalidUsage(Exception):
    pass


class SchemaValidationError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class ValidationError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "ValidationError": {
        "message": "Something went wrong",
        "status": 400
    },
    "UnauthorizedError": {
        "message": "Invalid username or password",
        "status": 401
    },

    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "InvalidUsage": {
        "message": "Invalid usage errors",
        "status": 400
    }
}

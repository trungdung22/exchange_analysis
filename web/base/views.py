from flask_restful import Resource, Api, reqparse
from flask import jsonify, make_response


class BaseResource(Resource):
    """Base resorouce controller class"""
    parser = reqparse.RequestParser()

    def add_filter(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def get_filter(self, *args, **kwargs):
        return self.parser.parse_args(*args, **kwargs)

    def success(self, data=None):
        return make_response(jsonify({'data': data}), 200)

    def error(self, error_code=403, message="Exception occur."):
        return make_response(jsonify({'message': message}), error_code)

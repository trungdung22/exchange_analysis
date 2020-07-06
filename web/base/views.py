from flask_restful import Resource, Api, reqparse


class BaseResource(Resource):
    """Base resorouce controller class"""
    parser = reqparse.RequestParser()

    def add_filter(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def get_filter(self, *args, **kwargs):
        return self.parser.parse_args(*args, **kwargs)

    def success(self, data=None):
        return {'data': data}, 201

    def error(self, error_code=403, message="Exception occur."):
        return {'message': message}, error_code

from flask import jsonify, Blueprint, abort
from flask_restful import (Resource, Api, reqparse, fields, marshal, marshal_with, url_for)
import models

quote_fields = {
    'id': fields.Integer,
    'quote': fields.String,
    'attributed_to': fields.String,
    'medium': fields.String
}


class Quote(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'quote',
            required=False,
            help='No quote provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'attributed_to',
            required=False,
            help='No author provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'medium',
            required=False,
            help='No medium provided',
            location=['form', 'json']
        )    
        super().__init__()
    @marshal_with(quote_fields)
    def get(self, id):
        try:
            quote = models.Quote.get(models.Quote.id==id)
        except models.Quote.DoesNotExist:
            abort(404)
        else:
            return (quote, 200)
    @marshal_with(quote_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Quote.update(**args).where(models.Quote.id==id)
        query.execute()
        print(query)
        return (models.Quote.get(models.Quote.id==id), 200)

    def delete(self, id):
        query = models.Quote.delete().where(models.Dog.id==id)
        query.execute()
        return {"message": "resource deleted"}


quotes_api = Blueprint('resources.quotes', __name__)

api = Api(quotes_api)

api.add_resource(
    Quote,
    '/quotes/<int:id>',
    endpoint='quote'
)
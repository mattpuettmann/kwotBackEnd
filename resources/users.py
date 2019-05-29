import json
from flask import jsonify, Blueprint, abort, make_response
from flask_restful import Resource, Api, reqparse, inputs, fields, marshal, marshal_with, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash, bcrypt
import models

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'password': fields.String,
    'verify_password': fields.String
}

class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help='No password verification provided',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(user_fields)
    def get(self):
        new_users = [marshal(user, user_fields) for user in models.User.select()]
        return (new_users, 201)

    def post(self):
        args = self.reqparse.parse_args()
        if args['password'] == args['verify_password']:
            print(args)
            user = models.User.create_user(**args)
            login_user(user)
            return marshal(user, user_fields), 201
        return make_response(
            json.dumps({
                'error': 'Password and password verification do not match'
            }), 400)



class AuthList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(user_fields)
    def get(self):
        new_users = [marshal(user, user_fields) for user in models.User.select()]
        return (new_users, 201)

    @marshal_with(user_fields)
    def post(self):
        print('user login route hit')
        args = self.reqparse.parse_args()
        print(args)
        user = models.User.get(username=args.username)
        candidate = args['password']
        check = check_password_hash(user.password, candidate)
        print(check)
        if check == True:
            print(user.username, 'this is the user object')
            print(args.password, 'this is args pw')
            login_user(user)
            return marshal(user, user_fields), 201

        print('wrong password ya goof!')

        # return make_response(
        #     print()
        #     json.dumps({
        #         'error': 'Password and password verification do not match'
        #     }), 400)
        



users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    UserList,
    '/registration',
    endpoint='users'
)
api.add_resource(
    AuthList,
    '/login',
    endpoint='user'
)
from flask import Blueprint, request

from flask_cors import CORS, cross_origin

from Service.Auth import login_user, register_user

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['POST'])
@cross_origin(origin='*')
def login():
    return login_user(request.json['username'], request.json['password'])


@auth_blueprint.route('/register', methods=['POST'])
def register():
    return register_user(request.json['username'], request.json['password'], request.json['nickname'])

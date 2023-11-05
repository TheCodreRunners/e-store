import json
import os

from flask import Blueprint, request
import jwt
from flask_cors import CORS, cross_origin

from Models.models import UserLogin
from Service.Auth import login_user, register_user

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['POST'])
@cross_origin(origin='*')
def login():
    return login_user(request.json['username'], request.json['password'])


@auth_blueprint.route('/register', methods=['POST'])
def register():
    return register_user(request.json['username'], request.json['password'], request.json['nickname'])

@auth_blueprint.route('/getuser', methods=['GET'])
def getuser():
    jwtkey = os.environ.get('JWT_SECRET_KEY')
    decodeddata = jwt.decode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTIxNjc3MCwianRpIjoiOTQyNjRlMjItODcyNy00OWY0LThiMDgtY2ExYzE0MDZmMWEyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IndpbGxpYW11bGd1aW1AZ21haWwuY29tIiwibmJmIjoxNjk5MjE2NzcwfQ.MA3t0GnVvD7Tu2hS3bQd3ayRkFYTDUK8r6A3eMMklIA",
                      jwtkey, algorithms=["HS256"]        )
    user = UserLogin.query.filter_by(username=decodeddata['sub']).first()
    return json.dumps(user.serialize())

from flask import Flask,Blueprint, render_template, abort,jsonify, request

from Auth.twAuth import twit_auth
from Service.games import get_games, get_game, create_game, create_publisher, get_publishers, delete_game, \
    delete_publisher
from flask import session

import json

# Blueprint Configuration
games_blueprint = Blueprint('games', __name__)


@games_blueprint.route('/', methods=['GET','POST',"PUT"])
def hi_there():
    try:
        twich_key = twit_auth()
        token = twich_key['access_token']
        session['twich_key'] = str(token)
        print(twich_key)
        return 'twich_key'
    except Exception as e:
        return json.dumps({'error': str(e)})


@games_blueprint.route('/games', methods=['GET','POST'])
def games_list():
    if request.method == 'GET':
        return get_games()
    elif request.method == 'POST':
        return create_game(request)


@games_blueprint.route('/games/<id>', methods=['GET','POST',"PUT","DELETE"])
def games(id):
    if request.method == 'GET':
        return get_game(id)
    elif request.method == 'DELETE':
        return delete_game(id)
    elif request.method == 'PUT':
        return create_game(request)


@games_blueprint.route('/publisher/<id>', methods=['GET','POST',"PUT","DELETE"])
def publisher(id):
    if request.method == 'GET':
        return get_publishers()
    elif request.method == 'POST':
        return create_publisher(request)
    elif request.method == 'DELETE':
        return delete_publisher(id)




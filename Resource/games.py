from flask import Flask, Blueprint, render_template, abort, jsonify, request

from Auth.twAuth import twit_auth
from Service.games import get_games, get_game, create_game, create_publisher, get_publishers, delete_game, \
    delete_publisher, update_game, get_gamescountbycategory, get_gamescountByPublisher, general_stats
from flask import session
from flask_cors import CORS, cross_origin
import json

# Blueprint Configuration
games_blueprint = Blueprint('games', __name__)


@games_blueprint.route('/', methods=['GET', 'POST', "PUT"])
@cross_origin(origin='*')
def hi_there():
    try:
        twich_key = twit_auth()
        token = twich_key['access_token']
        session['twich_key'] = str(token)
        print(twich_key)
        return 'twich_key'
    except Exception as e:
        return json.dumps({'error': str(e)})


@games_blueprint.route('/games', methods=['GET', 'POST'])
@cross_origin(origin='*')
def games_list():
    if request.method == 'GET':
        return get_games()
    elif request.method == 'POST':
        return create_game(request)


@games_blueprint.route('/games/<id>', methods=['GET', 'POST', "PUT", "DELETE"])
@cross_origin(origin='*')
def games(id):
    if request.method == 'GET':
        return get_game(id)
    elif request.method == 'DELETE':
        return delete_game(id)
    elif request.method == 'PUT':
        return update_game(id, request)


@games_blueprint.route('/gamescountbycategory', methods=['GET'])
@cross_origin(origin='*')
def gamescountbycategory():
    if request.method == 'GET':
        return get_gamescountbycategory()


@games_blueprint.route('/gamescountbypublisher', methods=['GET'])
@cross_origin(origin='*')
def gamescountbypublisher():
    if request.method == 'GET':
        return get_gamescountByPublisher()


@games_blueprint.route('/generalstats', methods=['GET'])
@cross_origin(origin='*')
def generalstats():
    if request.method == 'GET':
        return general_stats()


@games_blueprint.route('/publisher/<id>', methods=['GET', 'POST', "PUT", "DELETE"])
@cross_origin(origin='*')
def publisher(id):
    if request.method == 'GET':
        return get_publishers()
    elif request.method == 'POST':
        return create_publisher(request)
    elif request.method == 'DELETE':
        return delete_publisher(id)


@games_blueprint.route('/publishers', methods=['GET'])
@cross_origin(origin='*')
def publishers():
    if request.method == 'GET':
        return get_publishers()

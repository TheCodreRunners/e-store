from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from Service.itens import get_item, create_item, create_publisher, get_publishers, delete_item, \
    delete_publisher, update_item, general_stats, get_items

from flask_cors import cross_origin
import json

# Blueprint Configuration
itens_blueprint = Blueprint('itens', __name__)


@itens_blueprint.route('/', methods=['GET', 'POST', "PUT"])
@cross_origin(origin='*')
def hi_there():
    try:
        return 'twich_key'
    except Exception as e:
        return json.dumps({'error': str(e)})


@itens_blueprint.route('/itens', methods=['GET', 'POST'])
@cross_origin(origin='*')
def games_list():
    if request.method == 'GET':
        return get_items()
    elif request.method == 'POST':
        return create_item(request)


@itens_blueprint.route('/item/<id>', methods=['GET', 'POST', "PUT", "DELETE"])
@cross_origin(origin='*')
def games(id):
    if request.method == 'GET':
        return get_item(id)
    elif request.method == 'DELETE':
        return delete_item(id)
    elif request.method == 'PUT':
        return update_item(id, request)


@itens_blueprint.route('/generalstats', methods=['GET'])
@cross_origin(origin='*')
def generalstats():
    if request.method == 'GET':
        return general_stats()


@itens_blueprint.route('/publisher/<id>', methods=['GET', "PUT", "DELETE"])
@cross_origin(origin='*')
def publisher(id):
    if request.method == 'GET':
        return get_publishers()
    elif request.method == 'POST':
        return create_publisher(request)
    elif request.method == 'DELETE':
        return delete_publisher(id)


@itens_blueprint.route('/publishers', methods=['GET', 'POST'])
@cross_origin(origin='*')
def publishers():
    if request.method == 'GET':
        return get_publishers()
    if request.method == 'POST':
        return create_publisher(request)

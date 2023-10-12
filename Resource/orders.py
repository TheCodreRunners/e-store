from flask import Blueprint, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from Service.orders import get_orders, create_orders, get_order

order_blueprint = Blueprint('orders', __name__)


@order_blueprint.route('/orders', methods=['POST', 'GET'])
@jwt_required()
@cross_origin(origin='*')
def orders():
    if request.method == 'GET':
        return get_orders()
    elif request.method == 'POST':
        return create_orders(request)


@order_blueprint.route('/order/<id>', methods=['GET'])
@jwt_required()
@cross_origin(origin='*')
def order(id):
    if request.method == 'GET':
        return get_order(id)

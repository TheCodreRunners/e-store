from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from Service.orders import get_orders, create_orders

order_blueprint = Blueprint('orders', __name__)


@order_blueprint.route('/orders', methods=['POST', 'GET'])
@jwt_required()
def orders():
    if request.method == 'GET':
        return get_orders()
    elif request.method == 'POST':
        return create_orders(request)

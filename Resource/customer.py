import stripe
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from Service.customer import create_customer, get_customers


from flask_cors import cross_origin


# Blueprint Configuration
customer_blueprint = Blueprint('customer', __name__)

@customer_blueprint.route('/customer', methods=['POST', 'GET'])
@cross_origin(origin='*')
@jwt_required()
def customer():
    if request.method == 'POST':
        return create_customer(request)
    elif request.method == 'GET':
        return get_customers()
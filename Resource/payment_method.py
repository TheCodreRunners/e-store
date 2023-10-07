from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from Service.customer import get_customers
from Service.payment_method import create_paymentmethod

from flask_cors import cross_origin

payment_method = Blueprint('payment_method', __name__)


@payment_method.route('/payment_method', methods=['POST', 'GET'])
@cross_origin(origin='*')
@jwt_required()
def payment():
    if request.method == 'POST':
        return create_paymentmethod(request)
    elif request.method == 'GET':
        return get_customers()
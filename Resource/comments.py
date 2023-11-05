import stripe
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from Service.comments import get_commentsEval, create_commentsEval
from Service.customer import create_customer, get_customers

from flask_cors import cross_origin

# Blueprint Configuration
comments_blueprint = Blueprint('comments', __name__)


@comments_blueprint.route('/comments', methods=['POST', 'GET'])
@cross_origin(origin='*')
@jwt_required()
def customer():
    if request.method == 'POST':
        return create_commentsEval(request)
    elif request.method == 'GET':
        return get_commentsEval()

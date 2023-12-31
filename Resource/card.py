from flask import Flask, Blueprint, render_template, abort, jsonify, request

from flask_jwt_extended import jwt_required

from Service.cards import create_card, get_cards


from flask_cors import  cross_origin



cards_blueprint = Blueprint('cards', __name__)



@cards_blueprint.route('/cards', methods=['GET', 'POST', "PUT"])
@cross_origin(origin='*')
@jwt_required()
def cards():
    if request.method == 'GET':
        return get_cards()
    elif request.method == 'POST':
        return create_card(request)
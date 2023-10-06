import json
import sys

from flask import jsonify
from sqlalchemy import func
from sqlalchemy.sql import text
from Models.models import CreditCard, Item, Publisher, database as db
import stripe
import os



def create_card(request):
    try:
        data = request.get_json()

        card = CreditCard(**data)
        db.session.add(card)
        db.session.commit()
        # stripe.Card.create(data)
        return json.dumps(card.serialize())
    except Exception as e:
        db.session.rollback()
        return json.dumps({'error': str(e),})

def get_cards():
    try:
        cards = CreditCard.query.all()
        if cards is None:
            return json.dumps({'error': 'cards not found'})
        serialized_cards = [card.serialize() for card in cards]
        return json.dumps(serialized_cards)
    except Exception as e:
        return json.dumps({'error': str(e)})
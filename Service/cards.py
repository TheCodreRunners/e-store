import json

import stripe

from Models.models import CreditCard, database as db, Customer


def create_card(request):
    try:
        data = request.get_json()
        creditcard = data['source']
        clientId = data['clientId']
        client = Customer.query.filter_by(id=clientId).first()
        res = stripe.Customer.create_source(client.stripe_customer_id, source=creditcard)
        card = CreditCard(user_id=clientId, name=res.name, address_city=res.address_city,
                          address_country=res.address_country, address_line1=res.address_line1,
                          address_line1_check=res.address_line1_check, address_line2=res.address_line2,
                          address_state=res.address_state, address_zip=res.address_zip,
                          address_zip_check=res.address_zip_check, country=res.country, brand=res.brand,
                          customer=res.customer, exp_month=res.exp_month, exp_year=res.exp_year, funding=res.funding,
                          last4=res.last4, dynamic_last4=res.dynamic_last4, tokenization_method=res.tokenization_method,
                          wallet=res.wallet, cvc_check=res.cvc_check, fingerprint=res.fingerprint)
        db.session.add(card)
        db.session.commit()
        return json.dumps(res)
    except Exception as e:
        db.session.rollback()
        return json.dumps({'error': str(e), })


def get_cards():
    try:
        cards = CreditCard.query.all()
        if cards is None:
            return json.dumps({'error': 'cards not found'})
        serialized_cards = [card.serialize() for card in cards]
        return json.dumps(serialized_cards)
    except Exception as e:
        return json.dumps({'error': str(e)})

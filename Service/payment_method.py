import json
import sys

import stripe

from Models.models import PaymentMethod, database as db, Customer


def create_paymentmethod(request):
    try:
        data = request.get_json()
        customer = Customer.query.filter_by(id=data['customerId']).first()
        stripe_customer_id = customer.stripe_customer_id
        type = data['paymentMethodType']
        card = {"number": data['number'], "exp_month": data['exp_month'], "exp_year": data['exp_year'],
            "cvc": data['cvc'], }
        paymenthMethod = PaymentMethod(customer_stripe_id=stripe_customer_id, customerId=data['customerId'],
                                       paymentMethodType=type)
        db.session.add(paymenthMethod)
        db.session.commit()
        res = stripe.PaymentMethod.create(card=card, type=type)
        print(type, file=sys.stderr)
        stripe.PaymentMethod.attach(res.id, customer=stripe_customer_id, )
        return json.dumps(paymenthMethod.serialize())
    except Exception as e:
        db.session.rollback()
        return json.dumps({'error': str(e), })

def get_paymentmethods():
    try:
        paymenthMethods = PaymentMethod.query.all()
        return json.dumps([paymenthMethod.serialize() for paymenthMethod in paymenthMethods])
    except Exception as e:
        return json.dumps({'error': str(e), })

def get_paymentmethod(id):
    try:
        paymenthMethod = PaymentMethod.query.filter_by(id=id).first()
        return json.dumps(paymenthMethod.serialize())
    except Exception as e:
        return json.dumps({'error': str(e), })
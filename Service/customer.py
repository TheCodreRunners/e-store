import json
import sys

import stripe

from Models.models import CreditCard, database as db, Customer, UserLogin


def create_customer(request):
    try:
        data = request.get_json()
        userId = data['user_id']
        user = UserLogin.query.filter_by(id=userId).first()

        res = stripe.Customer.create(
        email=user.username, name=user.nickname,
        help="Needed to identify the customer on stripe")
        customer = Customer(user_id=userId, stripe_customer_id=res.id)
        db.session.add(customer)
        db.session.commit()
        return json.dumps({'success': True})
    except Exception as e:
        db.session.rollback()
        return json.dumps({'error': str(e), })


def get_customers():
    try:
        customers = Customer.query.all()
        if customers is None:
            return json.dumps({'error': 'customers not found'})
        serialized_customers = [customer.serialize() for customer in customers]
        return json.dumps(serialized_customers)
    except Exception as e:
        return json.dumps({'error': str(e)})

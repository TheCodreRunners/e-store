import json


import stripe

from Models.models import Orders, database as db, Item, OrderDetail


def get_orders():
    try:
        orders = Orders.query.join(OrderDetail).all()

        if orders is None:
            return json.dumps({'error': 'orders not found'})
        serialized_orders = [order.serialize() for order in orders]
        return json.dumps(serialized_orders)

    except Exception as e:
        return json.dumps({'error': str(e)})


def get_order(id):
    try:
        order = Orders.query.filter_by(id=id).first_or_404()
        return json.dumps(order.serialize())
    except Exception as e:
        return json.dumps({'error': str(e)})


def create_orders(request):
    try:
        customer_id= request.json['customer_id']
        order = Orders(customer_id=customer_id, status='status')
        items = request.json['item']
        line_items = []

        for item in items:

            i = Item.query.filter_by(id=item['item_id']).first()
            order.order_detail.append(OrderDetail(item=i, quantity=item['quantity']))
            ## The price should be The stripe price id

            line_items.append({
                "price": i.stripe_price_id,
                "quantity": item['quantity'],
                # "currency": "brl"
            })

        stripe.checkout.Session.create(line_items=line_items,payment_method_types=['card'], mode="payment",  success_url="https://example.com/success",
)
        # @classmethod

        db.session.add(order)
        db.session.commit()
        return json.dumps(order.serialize())
    except Exception as e:
        db.session.rollback()
        return json.dumps({'error': str(e)})

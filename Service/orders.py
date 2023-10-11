import json
import sys



from Models.models import Orders, database as db, Item


def get_orders():
    try:
        orders = Orders.query.all()
        for order in orders:
            print(order.serialize(), file=sys.stderr)

        if orders is None:
            return json.dumps({'error': 'orders not found'})
        serialized_orders = [order.serialize() for order in orders]
        return json.dumps(serialized_orders)

    except Exception as e:
        return json.dumps({'error': str(e)})


def create_orders(request):
    try:
        user = request.json

        itens = request.json['item']
        # print(itens, file=sys.stderr)
        order = Orders(customer_id=user['customer_id'], status=user['status'])

        for item_data in itens:
            item = Item(name=item_data['name'], quantity=item_data['quantity'])
            order.items.append(item)

        # res.item = [itens]

        db.session.add(res)
        db.session.commit()
        return json.dumps(res.serialize() for res in res)
    except Exception as e:
        db.session.rollback()
        print(e, file=sys.stderr)
        return json.dumps({'error': str(e)})

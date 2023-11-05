import json
import sys

from flask import jsonify
from sqlalchemy import func
from sqlalchemy.sql import text

from Models.models import Item, Publisher, database as db, Orders
import stripe
import os
import pickle
stripe.api_key = os.environ.get('STRIPE_API_KEY')


def serialize_any(obj):
    if isinstance(obj, Item):
        return obj.serialize()
    elif isinstance(obj, Publisher):
        return obj.serialize()
    else:
        return None


# items
def get_items(field="created_at", order="asc"):
    try:
        items = Item.query.order_by(text(f"{field} {order}")).paginate(per_page=10, max_per_page=10)
        if items is None:
            return json.dumps({'error': 'items not found'})

        serialized_items = items
        print(items.items, file=sys.stderr)
        # items = pickle.dumps(items)
        paginated_items = {
            "page": items.page,
            "pages": items.pages,
            "per_page": items.per_page,
            "has_next": items.has_next,
            "has_prev": items.has_prev,
            "total": items.total,
            "items": [serialize_any(item) for item in items.items]
        }
        return json.dumps(paginated_items)
    except Exception as e:
        return json.dumps({'error': str(e)})


def get_item(id):
    try:
        item = Item.query.filter_by(id=id).first()
        return json.dumps(item.serialize())
    except Exception as e:
        return json.dumps({'error': str(e)})


def delete_item(id):
    try:
        item = Item.query.filter_by(id=id).first()
        db.session.delete(item)
        db.session.commit()

        stripe.Product.delete(str(id))
        return json.dumps({'success': True})
    except Exception as e:
        db.session.rollback()
        return json.dumps({'error': str(e)})


def update_item(id, request):
    try:
        item = Item.query.filter_by(id=id).first()
        item.name = request.json['name']
        item.description = request.json['description']
        item.price = request.json['price']
        item.image = request.json['image']
        item.category = request.json['category']
        item.publisher_id = request.json['publisher_id']
        item.upcoming = request.json['upcoming']
        db.session.commit()
        return jsonify(item)
    except Exception as e:
        return json.dumps({'error': str(e)})


def create_item(request):
    try:
        item = Item(request.json['name'], request.json['description'], request.json['price'], request.json['image'],
                    request.json['category'], request.json['upcoming'])

        default_price = {
            'currency': 'brl',
            'unit_amount_decimal': int(item.price * 100),
        }

        res = stripe.Product.create(name=item.name, description=item.description,
                                    default_price_data=default_price)

        item.stripe_price_id = res.default_price

        db.session.add(item)
        db.session.commit()

        # return res
        return json.dumps(serialize_any(item))
    except Exception as e:
        db.session.rollback()
        return json.dumps({'error': str(e)})


def get_publishers():
    try:
        publishers = Publisher.query.all()
        serialized_publishers = [publisher.serialize() for publisher in publishers]
        return json.dumps(serialized_publishers)

    except Exception as e:
        return json.dumps({'error': str(e)})



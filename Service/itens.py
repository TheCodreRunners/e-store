import json
import sys

from flask import jsonify
from sqlalchemy import func
from sqlalchemy.sql import text


from Models.models import Item, Publisher, database as db , Orders
import stripe
import os

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
        items = Item.query.order_by(text(f"{field} {order}")).all()
        if items is None:
            return json.dumps({'error': 'items not found'})
        # serialized_items = [item.serialize() for item in items]
        print(items, file=sys.stderr)
        serialized_items = items
        return json.dumps(serialized_items)
    except Exception as e:
        return json.dumps({'error': str(e)})


def get_item(id):
    try:
        item = Item.query.filter_by(id=id).first()
        return json.dumps(item.serialize())
    except Exception as e:
        return json.dumps({'error': str(e)})


def get_itemscountbycategory():
    try:
        items = Item.query.with_entities(item.category, db.func.count(item.category)).group_by(item.category).all()

        newList = [['category', 'count']]
        for item in items:
            newList.append(list(item))

        return json.dumps(newList)
    except Exception as e:
        return json.dumps({'error': str(e)})


def get_itemscountByPublisher():
    try:
        items = db.session.query(Publisher.name, func.count(Item.id)).join(Item,
                                                                           Publisher.id == Item.publisher_id).group_by(
            Publisher.name).all()
        newList = [['publisher', 'count']]
        for item in items:
            newList.append(list(item))

        return json.dumps(newList)
    except Exception as e:
        return json.dumps({'error': str(e)})


def general_stats():
    try:
        total_items = Item.query.count()
        total_value = Item.query.with_entities(func.sum(Item.price)).first()[0]
        total_publishers = Publisher.query.count()
        return json.dumps(
            {'total_items': total_items, 'total_value': total_value, 'total_publishers': total_publishers})
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
        db.session.add(item)
        db.session.commit()
        default_price = {
            'currency': 'brl',
            'unit_amount_decimal': int(item.price * 100),
        }
        stripe.Product.create(id=str(item.id), name=item.name, description=item.description,
                              default_price_data=default_price)
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


def create_publisher(request):
    try:
        publisher = Publisher(request.json['name'], request.json['description'], request.json['image'])
        db.session.add(publisher)
        db.session.commit()
        return jsonify(publisher)
    except Exception as e:
        return json.dumps({'error': str(e)})


def delete_publisher(id):
    try:
        publisher = Publisher.query.filter_by(id=id).first()
        db.session.delete(publisher)
        db.session.commit()

        return json.dumps({'success': True})
    except Exception as e:
        db.session.rollback()
        return json.dumps({'error': str(e)})

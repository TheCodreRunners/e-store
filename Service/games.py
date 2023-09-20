import json
import sys

from flask import jsonify
from sqlalchemy import func
from sqlalchemy.sql import text
from Models.models import Game, Publisher, database as db


# Games
def get_games(field="created_at", order="asc"):
    try:
        games = Game.query.order_by(text(f"{field} {order}")).all()
        if games is None:
            return json.dumps({'error': 'Games not found'})
        serialized_games = [game.serialize() for game in games]
        return json.dumps(serialized_games)
    except Exception as e:
        return json.dumps({'error': str(e)})


def get_game(id):
    try:
        game = Game.query.filter_by(id=id).first()
        return json.dumps(game.serialize())
    except Exception as e:
        return json.dumps({'error': str(e)})


def get_gamescountbycategory():
    try:
        games = Game.query.with_entities(Game.category, db.func.count(Game.category)).group_by(Game.category).all()

        newList = [['category', 'count']]
        for game in games:
            newList.append(list(game))

        return json.dumps(newList)
    except Exception as e:
        return json.dumps({'error': str(e)})


def get_gamescountByPublisher():
    try:
        games = db.session.query(Publisher.name, func.count(Game.id)).join(Game,
                                                                           Publisher.id == Game.publisher_id).group_by(
            Publisher.name).all()
        newList = [['publisher', 'count']]
        for game in games:
            newList.append(list(game))

        return json.dumps(newList)
    except Exception as e:
        return json.dumps({'error': str(e)})


def general_stats():
    try:
        total_games = Game.query.count()
        total_value = Game.query.with_entities(func.sum(Game.price)).first()[0]
        total_publishers = Publisher.query.count()
        return json.dumps(
            {'total_games': total_games, 'total_value': total_value, 'total_publishers': total_publishers})
    except Exception as e:
        return json.dumps({'error': str(e)})


def delete_game(id):
    try:

        game = Game.query.filter_by(id=id).first()
        db.session.delete(game)
        db.session.commit()
        return json.dumps({'success': True})
    except Exception as e:
        return json.dumps({'error': str(e)})


def update_game(id, request):
    try:
        game = Game.query.filter_by(id=id).first()
        game.name = request.json['name']
        game.description = request.json['description']
        game.price = request.json['price']
        game.image = request.json['image']
        game.category = request.json['category']
        game.publisher_id = request.json['publisher_id']
        game.upcoming = request.json['upcoming']
        db.session.commit()
        return jsonify(game)
    except Exception as e:
        return json.dumps({'error': str(e)})


def create_game(request):
    try:
        game = Game(request.json['name'], request.json['description'], request.json['price'], request.json['image'],
                    request.json['category'], request.json['publisher_id'], request.json['upcoming'])
        db.session.add(game)
        db.session.commit()
        return jsonify(game)
    except Exception as e:
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
        return json.dumps({'error': str(e)})

import json

from flask import jsonify

from Models.models import Game,Publisher, database as db


# Games
def get_games():
    try:
        games = Game.query.all()
        serialized_games = [game.serialize() for game in games]
        return json.dumps(serialized_games)
    except Exception as e:
        return json.dumps({'error': str(e)})


def get_game(id):
    try:
        game = Game.query.filter_by(id=id).first()
        return game
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
        db.session.commit()
        return jsonify(game)
    except Exception as e:
        return json.dumps({'error': str(e)})


def create_game(request):
    try:
        game = Game(request.json['name'], request.json['description'], request.json['price'], request.json['image'],
                    request.json['category'], request.json['publisher_id'])
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
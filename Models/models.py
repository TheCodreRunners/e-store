from enum import StrEnum
from db_config import database


# Login enum
class RoleEnum(StrEnum):
    ADMIN = 'ADMIN'
    USER = 'USER'


class UserLogin(database.Model):
    __tablename__ = 'User'
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(120), unique=True)
    password = database.Column(database.String())
    role = database.Column(database.String(), default=RoleEnum.USER.value)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.role = RoleEnum.USER

    def __repr__(self):
        return f'<UserLogin {self.username}>'


class Game(database.Model):
    __tablename__ = 'Game'
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(120), unique=True)
    description = database.Column(database.String())
    price = database.Column(database.Float())
    image = database.Column(database.String())
    category = database.Column(database.String())
    publisher_id = database.Column(database.Integer, database.ForeignKey('Publisher.id'), nullable=True)
    upcoming = database.Column(database.Boolean(), default=False, nullable=True)
    created_at = database.Column(database.DateTime, default=database.func.now())
    updated_at = database.Column(database.DateTime, default=database.func.now(), onupdate=database.func.now())

    def __init__(self, name, description, price, image, category, publisher_id, upcoming):
        self.name = name
        self.description = description
        self.price = price
        self.image = image
        self.category = category
        self.publisher_id = publisher_id
        self.upcoming = False

    def __repr__(self):
        return f'<Game {self.name}>'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image': self.image,
            'category': self.category,
            'publisher_id': self.publisher_id,
            'upcoming': self.upcoming,
            'publisher': self.publisher.serialize() if self.publisher else None
        }


class Publisher(database.Model):
    __tablename__ = 'Publisher'
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(120), unique=True)
    description = database.Column(database.String())
    image = database.Column(database.String())
    games = database.relationship('Game', backref='publisher', lazy=True)

    def __init__(self, name, description, image):
        self.name = name
        self.description = description
        self.image = image

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            # 'games': self.games
        }

    def __repr__(self):
        return f'<Publisher {self.name}>'


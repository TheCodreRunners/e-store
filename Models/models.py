from enum import StrEnum

from db_config import database
from dataclasses import dataclass


# Login enum
class RoleEnum(StrEnum):
    ADMIN = 'ADMIN'
    USER = 'USER'


class StatusEnum(StrEnum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'


class PaymentMethodEnum(StrEnum):
    card = 'card'
    boleto = 'boleto'
    pix = 'pix'


class UserLogin(database.Model):
    __tablename__ = 'User'
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(120), unique=True)
    nickname = database.Column(database.String(120), unique=False)
    password = database.Column(database.String())
    role = database.Column(database.String(), default=RoleEnum.USER.value)
    comments = database.relationship('CommentsEval')

    def __init__(self, username, password, nickname):
        self.username = username
        self.password = password
        self.nickname = nickname
        self.role = RoleEnum.USER

    def __repr__(self):
        return f'<UserLogin {self.username}>'

    def serialize(self):
        return {'id': self.id, 'username': self.username, 'nickname': self.nickname, 'role': self.role,
          }

@dataclass
class Item(database.Model):
    __tablename__ = 'items'
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(120))
    description = database.Column(database.String())
    price = database.Column(database.Float())
    stripe_price_id = database.Column(database.String())
    image = database.Column(database.String())
    category = database.Column(database.String())
    comments = database.relationship('CommentsEval')
    upcoming = database.Column(database.Boolean(), default=False, nullable=True)
    created_at = database.Column(database.DateTime, default=database.func.now())
    updated_at = database.Column(database.DateTime, default=database.func.now(), onupdate=database.func.now())
    def __repr__(self):
        return f'<items {self.name}>'

    def serialize(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'price': self.price,
            'image': self.image, 'category': self.category, 'upcoming': self.upcoming,
            'created_at': str(self.created_at),'comments': [comment.serialize() for comment in self.comments] if self.comments else None,

        }


class OrderDetail(database.Model):
    __tablename__ = 'order_detail'
    order_id = database.Column(database.Integer, database.ForeignKey('orders.id'), primary_key=True)
    item_id = database.Column(database.Integer, database.ForeignKey('items.id'), primary_key=True)
    quantity = database.Column(database.Integer, nullable=False)
    item = database.relationship('Item')

    def serialize(self):
        return {'order_id': self.order_id, 'item_id': self.item_id, 'quantity': self.quantity,
            'item': self.item.serialize() if self.item else None, }


class Orders(database.Model):
    __tablename__ = 'orders'
    id = database.Column(database.Integer, primary_key=True)
    customer_id = database.Column(database.Integer, database.ForeignKey('Customer.id'), nullable=False)
    order_detail = database.relationship('OrderDetail')
    status = database.Column(database.String(), default=StatusEnum.PENDING.value)
    created_at = database.Column(database.DateTime, default=database.func.now())

    def __init__(self, customer_id, status, item=None):
        if item is None:
            item = []
        self.customer_id = customer_id
        self.status = status
        self.item = item

    def serialize(self):
        return {'id': self.id, 'customer_id': self.customer_id,
            'order_detail': [order_detail.serialize() for order_detail in
                             self.order_detail] if self.order_detail else None, 'status': self.status,

        }

    def __repr__(self):
        return f'<orders {self.id}>'

@dataclass
class CommentsEval(database.Model):
    __tablename__ = 'comments'
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('User.id'), nullable=False)
    item_id = database.Column(database.Integer, database.ForeignKey('items.id'), nullable=False)
    comment = database.Column(database.String())
    rating = database.Column(database.Integer())
    created_at = database.Column(database.DateTime, default=database.func.now())

    def serialize(self):
        return {'id': self.id, 'user_id': self.user_id, 'item_id': self.item_id, 'comment': self.comment,
            'rating': self.rating, 'created_at': str(self.created_at),

        }

class Prices(database.Model):
    __tablename__ = 'Prices'
    id = database.Column(database.Integer, primary_key=True)
    item_id = database.Column(database.Integer, database.ForeignKey('items.id'), nullable=True)
    price = database.Column(database.Float())
    created_at = database.Column(database.DateTime, default=database.func.now())

    def __init__(self, item_id, price):
        self.item_id = item_id
        self.price = price

    def __repr__(self):
        return f'<Prices {self.id}>'


class CreditCard(database.Model):
    __tablename__ = 'Credit_Card'
    id = database.Column(database.Integer, primary_key=True)
    customer_id = database.Column(database.Integer, database.ForeignKey('Customer.id'), nullable=False)
    name = database.Column(database.String())
    cvc_check = database.Column(database.String())
    address_city = database.Column(database.String())
    address_country = database.Column(database.String())
    address_line1 = database.Column(database.String())
    address_line1_check = database.Column(database.String())
    address_line2 = database.Column(database.String())
    address_state = database.Column(database.String())
    address_zip = database.Column(database.String())
    address_zip_check = database.Column(database.String())
    country = database.Column(database.String())
    brand = database.Column(database.String())
    customer = database.Column(database.String())
    exp_month = database.Column(database.Integer())
    exp_year = database.Column(database.Integer())
    funding = database.Column(database.String())
    last4 = database.Column(database.String())
    dynamic_last4 = database.Column(database.String())
    tokenization_method = database.Column(database.String())
    fingerprint = database.Column(database.String())
    wallet = database.Column(database.String())
    created_at = database.Column(database.DateTime, default=database.func.now())

    def __init__(self, user_id, name, address_city, address_country, address_line1, address_line1_check, address_line2,
                 address_state, address_zip, address_zip_check, country, brand, customer, exp_month, exp_year, funding,
                 last4, dynamic_last4, tokenization_method, wallet, cvc_check, fingerprint):
        self.user_id = user_id
        self.name = name
        self.address_city = address_city
        self.address_country = address_country
        self.address_line1 = address_line1
        self.address_line1_check = address_line1_check
        self.address_line2 = address_line2
        self.address_state = address_state
        self.address_zip = address_zip
        self.address_zip_check = address_zip_check
        self.cvc_check = cvc_check
        self.country = country
        self.brand = brand
        self.customer = customer
        self.exp_month = exp_month
        self.exp_year = exp_year
        self.funding = funding
        self.last4 = last4
        self.dynamic_last4 = dynamic_last4
        self.fingerprint = fingerprint
        self.tokenization_method = tokenization_method
        self.wallet = wallet

    def serialize(self):
        return {'id': self.id, 'user_id': self.user_id, 'name': self.name, 'address_city': self.address_city,
            'address_country': self.address_country, 'address_line1': self.address_line1,
            'address_line1_check': self.address_line1_check, 'address_line2': self.address_line2,
            'address_state': self.address_state, 'address_zip': self.address_zip,
            'address_zip_check': self.address_zip_check, 'country': self.country, 'brand': self.brand,
            'customer': self.customer, 'exp_month': self.exp_month, 'exp_year': self.exp_year, 'funding': self.funding,
            'last4': self.last4, 'tokenization_method': self.tokenization_method, 'wallet': self.wallet, }

    def __repr__(self):
        return f'<Credit_Card {self.id}>'


class Customer(database.Model):
    __tablename__ = 'Customer'
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('User.id'), nullable=False)
    stripe_customer_id = database.Column(database.String())
    created_at = database.Column(database.DateTime, default=database.func.now())

    def __init__(self, user_id, stripe_customer_id):
        self.user_id = user_id
        self.stripe_customer_id = stripe_customer_id

    def serialize(self):
        return {'id': self.id, 'user_id': self.user_id, 'stripe_customer_id': self.stripe_customer_id, }

    def __repr__(self):
        return f'<Customer {self.id}>'


class PaymentMethod(database.Model):
    __tablename__ = 'Payment_Method'
    id = database.Column(database.Integer, primary_key=True)
    paymentMethodType = database.Column(database.String())
    customerId = database.Column(database.ForeignKey('Customer.id'), nullable=False)
    customer_stripe_id = database.Column(database.String())

    def __init__(self, paymentMethodType, customerId, customer_stripe_id):
        self.paymentMethodType = paymentMethodType
        self.customerId = customerId
        self.customer_stripe_id = customer_stripe_id

    def __repr__(self):
        return f'<Payment_Method {self.id}>'


class Publisher(database.Model):
    __tablename__ = 'Publisher'
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(120), unique=True)
    description = database.Column(database.String())
    image = database.Column(database.String())

    def __init__(self, name, description, image):
        self.name = name
        self.description = description
        self.image = image

    def serialize(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'image': self.image, }

    def __repr__(self):
        return f'<Publisher {self.name}>'

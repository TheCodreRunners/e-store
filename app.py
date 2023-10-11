from flasgger import Swagger
from flask import Flask
from flask import session
from flask_migrate import Migrate

from Resource.card import cards_blueprint
from flask_session import Session
from flask_jwt_extended import JWTManager

from Resource.customer import customer_blueprint

from Resource.itens import itens_blueprint
from Resource.orders import order_blueprint
from Auth.auth import auth_blueprint
from Resource.payment_method import payment_method
import os

def create_app():
    app = Flask(__name__)
    swagger = Swagger(app)
    app.register_blueprint(itens_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(cards_blueprint)
    app.register_blueprint(customer_blueprint)
    app.register_blueprint(payment_method)
    app.register_blueprint(order_blueprint)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://flask:flask@{os.environ.get("POSTGRES_HOST")}:5432/{os.environ.get("POSTGRES_DB")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')  # Change this!
    jwt = JWTManager(app)

    from Models.models import database as db
    db.init_app(app)
    migrate = Migrate(app, db)
    # Configuring the database
    # db = SQLAlchemy(app)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    Session(app)

    return app

if __name__ == "__main__":
    print('Creating app...')
    print('aq' +os.environ.get('POSTGRES_HOST'))
    print('Creating app...')

    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

import json

from Models.models import UserLogin, database as db
from flask_jwt_extended import create_access_token


def login_user(username, password):
    try:
        user = UserLogin.query.filter_by(username=username, password=password).first()
        if user is None:
            return json.dumps({'error': 'User not found'})
        else:
            access_token = create_access_token(identity=username,expires_delta=False)
            return json.dumps({'token': access_token})

    except Exception as e:
        return json.dumps({'error': str(e)})


def register_user(username, password,nickname):
    try:
        user = UserLogin(username=username, password=password,nickname=nickname)
        db.session.add(user)
        db.session.commit()
        return json.dumps({'success': True})
    except Exception as e:
        return json.dumps({'error': str(e)})

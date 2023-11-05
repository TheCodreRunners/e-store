import json
import sys

import stripe

from Models.models import CreditCard, database as db, Customer, UserLogin, Item, CommentsEval


def create_commentsEval(request):
    try:
        data = request.get_json()
        print(data, file=sys.stderr)
        user = UserLogin.query.filter_by(id=data['user_id']).first()
        item = Item.query.filter_by(id=data['item_id']).first()
        rating = data['rating']
        comment = data['comment']
        comment = CommentsEval(user_id=user.id, item_id=item.id, rating=rating, comment=comment)
        db.session.add(comment)
        db.session.commit()

        return json.dumps({'success': True})
    except Exception as e:
        db.session.rollback()
        return json.dumps({'error': str(e), })


def get_commentsEval():
    try:
        customers = CommentsEval.query.all()
        if customers is None:
            return json.dumps({'error': 'Comment not found'})
        serialized_customers = [customer.serialize() for customer in customers]
        return json.dumps(serialized_customers)
    except Exception as e:
        return json.dumps({'error': str(e)})

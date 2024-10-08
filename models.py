# models.py
from database import session, User

def get_user(user_id, username):
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        user = User(id=user_id, username=username)
        session.add(user)
        session.commit()
    return user

def update_balance(user_id, amount):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.balance += amount
        session.commit()

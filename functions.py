import time

import jwt
from flask import jsonify

from app import app, db
from models import User, Menu, Order, Chat


def is_username_unique(username):
    data = User.query.filter_by(public_id=username).first()
    if data:
        return False
    return True


def is_email_unique(email):
    if User.query.filter_by(email=email).first():
        return False
    return True


def verify_user(email, password):
    try:
        user = User.query.filter_by(email=email).first()
        if user.check_password(password):
            return user.public_id
        return False
    except Exception as e:
        print('[ERROR]:', e)
        return False


def return_user_from_token(token):
    data = jwt.decode(
        bytes(token, encoding='utf-8'),
        app.config['SECRET_KEY']
    )
    return User.query.filter_by(public_id=data['username']).first()


def return_error_message(error, status=400):
    status = int(status)
    if 400 <= status < 500:
        return jsonify({'message': error}), int(status)
    else:
        return jsonify({'message': error}), 400


def return_success_message(message, status=200):
    status = int(status)
    return jsonify({'message': message}), status


def return_pizza_menu():
    return Menu.query.all()


def return_pizza_data(pizza_id):
    return Menu.query.filter_by(id=pizza_id).first()


def add_status(pizza_id, user_id, status):
    pizza = return_pizza_data(pizza_id)
    order = Order(user_id=user_id, order_items=str(pizza_id), status=status, bill_amount=pizza.price)
    db.session.add(order)
    db.session.commit()


def add_chat(user_id, msg_recieved, msg_replied, recieved_time, replied_time):
    chat = Chat(user_id=user_id, message_recieved=msg_recieved, message_reply=msg_replied, recieved_time=recieved_time, reply_time=replied_time)
    db.session.add(chat)
    db.session.commit()

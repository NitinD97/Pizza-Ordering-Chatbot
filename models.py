from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    public_id = db.Column(db.String(50), unique=True, index=True)
    email = db.Column(db.String(70), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(200))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.String(100), index=True)
    order_items = db.Column(db.String(100))
    status = db.Column(db.String(50), index=True)
    bill_amount = db.Column(db.Integer)

    NOT_ACCEPTED_YET = 'NOT ACCEPTED YET'
    BEING_PREPARED = 'BEING PREPARED'
    OUT_FOR_DELIVERY = 'OUT FOR DELIVERY'
    DELIVERED = 'DELIVERED'


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.String(100), index=True)
    message_recieved = db.Column(db.String(500))
    recieved_time = db.Column(db.String(50))
    message_reply = db.Column(db.String(500))
    reply_time = db.Column(db.String(50))


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    pizza_name = db.Column(db.String(80), unique=True, index=True)
    image_url = db.Column(db.String(200))
    price = db.Column(db.Integer)

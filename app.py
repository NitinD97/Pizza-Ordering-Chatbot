import datetime
import json
import time
from functools import wraps
from threading import Thread

import jwt
from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_migrate import Migrate
from flask_socketio import SocketIO, send, join_room
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

import chatbot
from config import Config


BOT_NAME = 'YoYo Bot'

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
bootstrap = Bootstrap(app)
import functions
from models import User, Order


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token', None)

        if token is None:
            return functions.return_error_message('Token is missing!', 401)

        try:
            data = jwt.decode(
                bytes(token, encoding='utf-8'),
                app.config['SECRET_KEY']
            )
            current_user = User.query.filter_by(public_id=data['username']).first()
        except:
            return functions.return_error_message('Token is invalid', 401)
        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    token = request.cookies.get('x-access-token', None)
    menu = functions.return_pizza_menu()
    if token:
        current_user = functions.return_user_from_token(token)
        return render_template('index.html', user=current_user, menu=menu), 200
    return render_template('index.html', menu=menu), 200


@app.route('/logout', methods=['GET'])
def logout():
    resp = redirect(url_for('index'))
    resp.delete_cookie('x-access-token')
    return resp


@app.route('/login', methods=['POST'])
def login():
    data = request.form
    print(data)
    if not data:
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    email, password = data.get('email', None).lower(), data.get('password', None)
    username = functions.verify_user(email, password)
    if username:

        token = jwt.encode(
            {
                'username': username,
            }
            , app.config['SECRET_KEY']
        ).decode('utf-8')
        redr = redirect(url_for('index'))
        redr.set_cookie('x-access-token', token, expires=datetime.datetime.utcnow()+datetime.timedelta(minutes=5))
        return redr
    return redirect(url_for('index'))


@app.route('/register', methods=['GET'])
def register_user():
    return render_template('register.html')


@app.route('/create_user', methods=['POST'])
def register():

    data = request.form
    print(data)
    email, error = data['email'].lower(), None
    if not data['password'] == data['confirmPassword']:
        error = 'Passwords must be same.'
    elif not functions.is_username_unique(data['username']):
        error = 'Username must be unique.'
    elif not functions.is_email_unique(email):
        error = 'Email is already registered.'
    if error:
        return render_template('register.html')
    user = User(
        public_id=data['username'],
        name=data['name'],
        email=email,
    )
    try:
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        print('[ERROR]: ', e)
        return redirect(url_for('register'))


@app.route('/order', methods=['POST'])
def place_order():
    import json
    data = json.loads(request.get_data().decode('utf-8'))
    handle_message('Hi there, I see you ordered a pizza, Ill keep you updated on the status.', user_id=data['user_id'], bot=True)
    Thread(target=order_pizza,
           args=(data['id'], data['user_id'])).start()
    print(data)
    return make_response({'status': 'success'}), 200


@app.route('/signin', methods=['GET'])
def signin():
    return render_template('login.html')


@socketio.on('join')
def on_join(message, user_id):
    # username = user_id or ''
    room = user_id
    join_room(room)
    send(message + ' connected!', room=room)


@socketio.on('message')
def handle_message(message, user_id=None, bot=False):
    print('send message: ', user_id)
    response = None
    if bot:
        send('<b><u>' + BOT_NAME + ':</b></u> ' + message, room=user_id, namespace='/')
    else:
        send('<b><u>' + user_id + ':</b></u> ' + message, room=user_id, namespace='/')
        response = chat(message)
    recieved_time = datetime.datetime.utcnow()
    reply_time = None
    if response:
        time.sleep(1)
        send('<b><u>'+BOT_NAME+':</b></u> '+response, room=user_id, namespace='/')
    functions.add_chat(user_id,message, response, recieved_time, reply_time)


def chat(msg):
    resp = chatbot.get_bot_response(msg)
    print(resp)
    final = ''
    for res in resp:
        final = final + res + '<br/>'
    return final

def order_pizza(pizza_id, user_id):
    pizza = functions.return_pizza_data(pizza_id)
    with app.test_request_context():

        status = 'You ordered: %s pizza<br> status: %s' % (pizza.pizza_name, 'Waiting for restaurant to accept')
        functions.add_status(pizza_id=pizza_id, user_id=user_id, status=Order.NOT_ACCEPTED_YET)
        handle_message(status, user_id, bot=True)
        time.sleep(10)

        functions.add_status(pizza_id=pizza_id, user_id=user_id, status=Order.BEING_PREPARED)
        status = 'Order status: %s' % 'In kitchen!'
        handle_message(status, user_id, bot=True)
        time.sleep(10)

        functions.add_status(pizza_id=pizza_id, user_id=user_id, status=Order.OUT_FOR_DELIVERY)
        status = 'Order status: %s' % 'Out for delivery'
        handle_message(status, user_id, bot=True)
        time.sleep(10)

        functions.add_status(pizza_id=pizza_id, user_id=user_id, status=Order.DELIVERED)
        status = 'Order status: %s' % 'Delivered'
        handle_message(status, user_id, bot=True)


if __name__ == '__main__':
    socketio.run(app)
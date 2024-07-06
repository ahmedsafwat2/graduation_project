import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

import random
import time
import paho.mqtt.client as mqtt_client

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)


def calc(speed, length, width, seeds):
    no_of_lines = int(width * 100 / seeds)
    length_of_line = int(length * 100 - 10)
    my_list=[]
    for i in range(1, no_of_lines + 1):
        my_list.append(('X', 10))
        my_list.append(('Z', 1))
        my_list.append(('E', .5))
        my_list.append(('P', .5))
        my_list.append(('U', int(length_of_line/speed)))
        my_list.append(('e', .5))
        my_list.append(('p', .5))
        my_list.append(('S', 3))
        my_list.append(('Y', 10))
        my_list.append(('Z', 1))
        if i % 2 == 0:
            my_list.append(('L', 2))
            my_list.append(('S', 3))
        else:
            my_list.append(('R', 2))
            my_list.append(('S', 3))
        my_list.append(('U', int(seeds/speed)))
        my_list.append(('S', 3))
        if i % 2 == 0:
            my_list.append(('L', 2))
            my_list.append(('S', 3))
        else:
            my_list.append(('R', 2))
            my_list.append(('S', 3))
    my_list.append(('X', 10))
    my_list.append(('Z', 1))
    my_list.append(('E', .5))
    my_list.append(('P', .5))
    my_list.append(('U', int(length_of_line/speed)))
    my_list.append(('e', .5))
    my_list.append(('p', .5))
    my_list.append(('S', 3))
    my_list.append(('Y', 10))
    my_list.append(('Z', 1))
    print(my_list)
    return my_list


def connect_mqtt():
    client_id = f'publish-{random.randint(0, 1000)}'
    broker = '2.tcp.eu.ngrok.io'
    port = 15402
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, my_list):
    topic = "python"
    time.sleep(3)
    while my_list:
        msg = my_list.pop(0)
        msg_l = msg[0]
        msg_t = msg[1]
        print(msg_l)
        result = client.publish(topic, msg_l)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        t1 = time.perf_counter()
        while (time.perf_counter() - t1) <= msg_t:
            pass

from flaskblog import routes

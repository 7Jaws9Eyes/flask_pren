
from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
import random
import json

app = Flask(__name__, static_url_path='', static_folder='build')
cors = CORS(app, resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def init():
    print("handle called")
    return app.send_static_file('index.html')

@app.route("/run")
def run():
    text = {
                "name": "Random Int 1",
                "number": random.randint(0, 1000)
            }
    return json.dumps(text)


def update_sensor_data(sensor_type, message):
    for x in range(600):
        data = {
            "name": sensor_type,
            "message": x
        }
        print(f"Updating sensor data type: {sensor_type} Data: {data['message']}")
        socketio.emit(sensor_type, json.dumps({"data": data}))
        x = x + 1


@socketio.event
def request():
    print('Data being requested')
    update_sensor_data('speed', 300)


@socketio.event
def event(data):
    print(f'event from client received {data}')
    socketio.emit('event', json.dumps(data))


@socketio.on('*')
async def catch_all(self, event, sid, data):
    print("catch all")
    pass


@socketio.on('connect')
def connect():
    print('connect ')


@socketio.on('disconnect')
def disconnect():
    print('disconnect ')


print(f'main.py called, name: {__name__}')

if __name__ == '__main__' or __name__ == 'app.main':
    print('socketio starting')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)


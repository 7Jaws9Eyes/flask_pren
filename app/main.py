
from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
import random
import json

app = Flask(__name__, static_url_path='', static_folder='build')
# cors = CORS(app, resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app, cors_allowed_origins='*')


@app.route("/")
def init():
    print("handle called")
    return app.send_static_file('index.html')


@app.route("/run")
def run():
    data = {
                "name": "status",
                "status": "offline"
            }
    socketio.emit('status_request')
    return json.dumps(data)


def send_test_data(sensor_type, message):
    for x in range(600):
        data = {
            "name": sensor_type,
            "message": x
        }
        print(f"sending test_data to: {sensor_type} Data: {data['message']}")
        socketio.emit(sensor_type, json.dumps({"data": data}))
        x = x + 1


def update_sensor_data(sensor_type, message):
    data = {
        "name": sensor_type,
        "message": message
    }
    print(f"Updating sensor data type: {sensor_type} Data: {data['message']}")
    socketio.emit(sensor_type, json.dumps({"data": data}))


@socketio.event
def request_test_data():
    print('test data being requested')
    send_test_data('speed', 300)


@socketio.event
def event(data):
    print(f'event from client received {data}')
    socketio.emit('event', json.dumps(data))


@socketio.event
def speed(data):
    print(f'speed from client received {data}')
    socketio.emit('speed', json.dumps(data))


@socketio.event
def voltage_print(data):
    print(f'voltage_print from client received {data}')
    socketio.emit('voltage_print', json.dumps(data))\


@socketio.event
def coils(data):
    print(f'coils from client received {data}')
    socketio.emit('coils', json.dumps(data))


@socketio.event
def acceleration(data):
    print(f'acceleration from client received {data}')
    socketio.emit('acceleration', json.dumps(data))


@socketio.event
def acceleration(data):
    print(f'voltage_motor from client received {data}')
    socketio.emit('voltage_motor', json.dumps(data))


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


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)

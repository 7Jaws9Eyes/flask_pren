from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
import time

app = Flask(__name__, static_url_path='', static_folder='build')
cors = CORS(app, resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app, cors_allowed_origins='*')
start_time = 0


@app.route("/")
def init():
    return app.send_static_file('index.html')


@socketio.event
def change_speed(data):
    socketio.emit('change_speed_client', data)


@socketio.event
def event(data):
    socketio.emit('event', data)


@socketio.event
def start_timer():
    print('started')
    global start_time
    start_time = time.time()
    socketio.emit('timer_start', start_time)


@socketio.event
def stop_timer():
    global start_time
    print('stopped')
    stop_time = int(round(time.time() - start_time))
    socketio.emit('timer_stop', stop_time)


@socketio.event()
def request_time():
    socketio.emit('present_time', time.time() - start_time)


@socketio.event()
def request_start_time():
    socketio.emit('start_time', start_time)


@socketio.event
def sensor_update(data):
    global start_time
    # print(f'sensor update from client received {data}')
    socketio.emit(data['name'], data['message'])


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

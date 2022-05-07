import asyncio

from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
import json
import time

app = Flask(__name__, static_url_path='', static_folder='build')
cors = CORS(app, resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app, cors_allowed_origins='*')
start_time = time.time()
stop_time = time.time()
continue_time = False

@app.route("/")
def init():
    return app.send_static_file('index.html')


@app.route("/run")
def run():
    data = {
                "name": "status",
                "status": "offline"
            }
    # socketio.emit('status_request')
    return json.dumps(data)

@socketio.event
def change_speed(data):
    socketio.emit('change_speed_client', data)


@socketio.event
def event(data):
    socketio.emit('event', data)


# @socketio.event
# def start_timer():
#     print(f'timer started')
#     global start_time
#     global continue_time
#     start_time = time.time()
#     continue_time = True
#     asyncio.run(ud())
#     socketio.emit('start_time', start_time)

#
# @socketio.event
# def stop_timer():
#     global stop_time
#     global start_time
#     global continue_time
#     stop_time = time.time()
#     continue_time = False
#     print('stopped timer')
#     socketio.emit('final_time', stop_time-start_time)
#
#
# async def ud():
#     global continue_time
#     print('starting ud')
#     while continue_time:
#         print('still goin')
#         await update_time()
#
#
# async def update_time():
#     global start_time
#     print('going to sleep')
#     await asyncio.sleep(1)
#     t = time.time() - start_time
#     print(f'woke up in a new bugatti {t}')
#     socketio.emit('present_time', t)
#

@socketio.event
def sensor_update(data):
    print(f'sensor update from client received {data}')
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

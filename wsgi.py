from app.main import socketio, app
print("WSGI Called")

def app(env):
    print("Main Called")
    socketio.run(app)

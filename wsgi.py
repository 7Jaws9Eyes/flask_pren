from app.main import socketio, app
print("WSGI Called")

if __name__ == "__main__":
    # socketio.run(app)
    app.run()

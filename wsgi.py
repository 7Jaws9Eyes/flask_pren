from app.main import socketio, app

print(f"WSGI Called, name: {__name__}")
if __name__ == "__main__":
    # socketio.run(app)
    app.run()

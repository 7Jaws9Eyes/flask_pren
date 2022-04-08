import app.main as main
print("WSGI Called")

def app(env):
    print("Main Called")
    main.run()

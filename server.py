from flask_app.controllers import recipes, logins
from flask_app import app

if __name__== "__main__":  # lines 10 and 11 are required on all server.py files and will not run without them.
    app.run(debug=True)

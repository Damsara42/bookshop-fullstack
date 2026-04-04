# import flask
from flask import Flask
# allow frontend to connect (cors)
from flask_cors import CORS
# to connect auth routes
from routes.auth import auth_routes

#creating the app instance
app = Flask(__name__)
# front end conect
CORS(app)

# connecting auth route
app.register_blueprint(auth_routes, url_prefix = '/auth')

#testing route example
@app.route('/')
def home():
    return "bookshop backend running"


#enable auto reload
if __name__ == '__main__':
    app.run(debug=True)
# import flask
from flask import Flask
# allow frontend to connect (cors)
from flask_cors import CORS
# to connect auth routes
from routes.auth import auth_routes
# to add the database connection
from db import get_connection

#creating the app instance
app = Flask(__name__)
# front end conect
CORS(app)

# session
app.config['SECRET_KEY'] = 'abababbabnananansjdakasnndo137892%$&%*&'

# connecting auth route
app.register_blueprint(auth_routes, url_prefix = '/auth')

#testing route example
@app.route('/')
def home():
    return "bookshop backend running"

# database route checking
@app.route('/test-db')
def test_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        return "Database Connected"
    except Exception as e:
        return str(e)


#enable auto reload
if __name__ == '__main__':
    app.run(debug=True)
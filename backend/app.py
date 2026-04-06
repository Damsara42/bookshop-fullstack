# import flask
from flask import Flask
# allow frontend to connect (cors)
from flask_cors import CORS
# to connect auth routes
from routes.auth import auth_routes
# to add the database connection
from db import get_connection
# to connect to book routes
from routes.books import book_routes
# to connect to cart
from routes.cart import cart_route
# to connect to orders
from routes.orders import order_routes

#creating the app instance
app = Flask(__name__)
# front end conect
CORS(app)

# session
app.config['SECRET_KEY'] = 'abababbabnananansjdakasnndo137892%$&%*&'

# connecting auth route
app.register_blueprint(auth_routes, url_prefix = '/auth')
# connect to books route
app.register_blueprint(book_routes, url_prefix = '/books')
# connect to cart route
app.register_blueprint(cart_route, url_prefix = '/cart')
# connect to order routes
app.register_blueprint(order_routes, url_prefix='/orders')

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
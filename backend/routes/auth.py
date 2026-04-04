""" this is a example auth route
from flask import Blueprint

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/test')
def test():
    return "Auth route wrking"
"""
# blueprint allows me to organize app into senction for example all auth routes in one file
from flask import Blueprint, request, jsonify, session
from db import get_connection
import bcrypt

# this tell flask to group these routes under the name auth
auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/register', methods=['POST']) # post --> sending data to the server
def register():
    data = request.json #gets data from frontend

    # getting user data
    name = data['name']
    email = data['email']
    password = data['password']

    #password hashing
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # database interaction
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Users (NAME, EMAIL, PASSWORD) VALUES (?, ?, ?)", # ? --> prevents sql injection
        (name, email, hashed_pw)
    )

    conn.commit()
    conn.close()

    # return a msg to the frontend
    return jsonify({"message": "User Registered Successfully"})

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json # gets data from frontend

    # user data
    email = data['email']
    password = data['password']

    # database
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM USERS WHERE EMAIL IS ?"
        (email,)
    )
    user = cursor.fetchone()

    conn.close()

    if user: 
        stored_passowrd = user.password

        # comparison hash
        if bcrypt.checkpw(password.encode('utf-8'), stored_passowrd.encode('utf-8')):

            # create session
            session['user_id'] = user.USER_ID
            session['role'] = user.ROLE
            
            return jsonify({"message": "Login success"})
    
    return jsonify({"error": "Invalid credentials"}), 401

# authorization to protect routes
@auth_routes.route('/profile')
def profile():
    if 'user_id' not in session:
        return jsonify ({"error": "Unauthorized"}), 401
    
    return jsonify ({"message": "Welcome!"}), 200

""""
if session.get('role') != 'admin':
   return jsonify ({"error": "admin only"}), 403
"""
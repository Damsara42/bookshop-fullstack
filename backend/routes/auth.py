""" this is a example auth route
from flask import Blueprint

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/test')
def test():
    return "Auth route wrking"
"""
# blueprint allows me to organize app into senction for example all auth routes in one file
from flask import Blueprint, request, jsonify
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
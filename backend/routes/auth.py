from flask import Blueprint

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/test')
def test():
    return "Auth route wrking"
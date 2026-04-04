from flask import blueprint

auth_routes = blueprint('auth', __name__)

@auth_routes.route('/test')
def test():
    return "Auth route wrking"
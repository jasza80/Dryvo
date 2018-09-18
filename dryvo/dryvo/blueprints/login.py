import os
import flask
from flask import Blueprint
from flask_login import login_user
from flask_oauth import OAuth

from api.database.models.user import User
from api.utils import RouteError, jsonify_response
from extensions import login_manager


login_routes = Blueprint('login', __name__, url_prefix='/login')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@login_routes.route('/direct', methods=['POST'])
@jsonify_response
def direct_login():
    data = flask.request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()

    # Try to authenticate the found user using their password
    if user and user.check_password(data.get('password')):
        login_user(user, remember=True)
        return {'message': 'You logged in successfully.'}
    else:
        # User does not exist. Therefore, we return an error message
        raise RouteError('Invalid email or password.', 401)


@login_routes.route('/register', methods=['POST'])
@jsonify_response
def register():
    post_data = flask.request.get_json()
    email = post_data.get('email')
    name = post_data.get('name')
    # Query to see if the user already exists
    user = User.query.filter_by(email=email).first()
    if email and name and not user:
        # There is no user so we'll try to register them
        # Register the user
        password = post_data.get('password')
        user = User(email=email, password=password, name=name)
        user.save()

        # return a response notifying the user that they registered successfully
        return {'message': 'You registered successfully. Please log in.'}, 201
    else:
        # There is an existing user. We don't want to register users twice
        # Return a message to the user telling them that they they already exist
        raise RouteError('Can not create user.')


@login_routes.route('/facebook')
def facebook_login():
    pass

@login_routes.route('facebook_authorized')
@jsonify_response
def facebook_authorized():
    pass

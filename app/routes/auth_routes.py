from flask import Blueprint, request, jsonify, current_app
from app.utils.helpers import generate_jwt_token
from app.utils.db_helper import query_db
from bcrypt import hashpw, gensalt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if email and password:
        user = authenticate_user(email, password)

        if user:
            token = generate_jwt_token(user['email'], user['role_id'], user['id'])
            return jsonify({'token': token, 'role_id': user['role_id'], 'first_name' : user['first_name'], 'last_name' : user['last_name'] , 'user_id': user['id']})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    else:
        return jsonify({'message': 'Missing email or password'}), 400

def authenticate_user(email, password):
    query = "SELECT * FROM users WHERE email = %s"
    args = (email,)
    user = query_db(query, args, one=True)

    if user and check_password(password, user['password']):
        return user
    else:
        return None

def check_password(input_password, hashed_password):
    return hashpw(input_password.encode('utf-8'), hashed_password.encode('utf-8')) == hashed_password.encode('utf-8')

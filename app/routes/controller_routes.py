from flask import Blueprint, jsonify, request, current_app
from app.utils.helpers import token_required, superadmin_required
from app.utils.db_helper import query_db
from app.utils.helpers import clean_and_lower, generate_bcrypt_hash
from app.constants.roles import roles
from app.services.users import is_user_email_exits, is_emp_id_exits
from app.services.user_areas import insert_user_areas


controllers_bp = Blueprint('controllers', __name__)

@controllers_bp.route('/controller', methods=['POST'])
@token_required
@superadmin_required
def add_user(current_user):

    current_user_id = current_user['id']

    data = request.get_json()
    user_email = clean_and_lower(data['email'])
    user_emp_id = clean_and_lower(data.get('emp_id'))

    if is_user_email_exits(user_email):
        return jsonify({'message': 'User with this email already exists!'}), 400

    if is_emp_id_exits(user_emp_id):
        return jsonify({'message': 'User with this employee id already exists!'}), 400

    hashed_pass = generate_bcrypt_hash(data['password'])
    query = "INSERT INTO users (email, password, role_id, first_name, last_name, employee_id, created_by_user_id) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    args = (
        user_email, 
        hashed_pass,
        roles.get("CONTROLLER"), 
        clean_and_lower(data.get('first_name')), 
        clean_and_lower(data.get('last_name')), 
        user_emp_id,
        current_user_id
    )

    query_db(query, args, True, True)

    return jsonify({'message': 'User added successfully'}), 201


@controllers_bp.route('/controllers', methods=['GET'])
@token_required
def get_all_controllers(current_user):
    query = "SELECT id, first_name, last_name, email, employee_id, created_at FROM users WHERE role_id = 3 order by created_at desc"
    admins = query_db(query)

    if not admins:
        return jsonify([])

    return jsonify(admins)

@controllers_bp.route('/controllers/<int:user_id>', methods=['PUT'])
@token_required
@superadmin_required
def update_user(current_user, user_id):
    try:
        data = request.get_json()
    
        user = query_db("SELECT * FROM users WHERE id = %s", (user_id,), one=True)
        if user is None:
            return jsonify({'error': 'User not found'}), 404

        if data['password'] == None or data['password'] == "":
            query = """
                UPDATE users 
                SET 
                    email = %s, 
                    first_name = %s, 
                    last_name = %s, 
                    employee_id = %s
                WHERE 
                    id = %s
            """
            args = (
                clean_and_lower(data['email']),  
                clean_and_lower(data.get('first_name')), 
                clean_and_lower(data.get('last_name')), 
                clean_and_lower(data.get('emp_id')),
                user_id
            )
            query_db(query, args, False, True)
        else:

            hashed_pass = generate_bcrypt_hash(data['password'])
            query = """
                UPDATE users 
                SET 
                    email = %s, 
                    first_name = %s, 
                    last_name = %s, 
                    employee_id = %s, 
                    password = %s
                WHERE 
                    id = %s
            """
            args = (
                clean_and_lower(data['email']), 
                clean_and_lower(data.get('first_name')), 
                clean_and_lower(data.get('last_name')), 
                clean_and_lower(data.get('emp_id')),  
                hashed_pass,
                user_id
            )

            query_db(query, args, False, True)

        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

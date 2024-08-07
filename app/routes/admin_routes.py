from flask import Blueprint, jsonify, request, current_app
from app.utils.helpers import token_required, superadmin_required
from app.utils.db_helper import query_db
from app.utils.helpers import clean_and_lower, generate_bcrypt_hash
from app.constants.roles import roles
from app.services.users import update_planner, is_user_email_exits, is_emp_id_exits
from app.services.user_areas import insert_user_areas

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admins', methods=['GET'])
@token_required
@superadmin_required
def get_all_admins(current_user):
    query = """
            SELECT u.id, first_name, last_name, email, employee_id, zone_name, ua.zone_id, created_at 
            FROM users u
            INNER JOIN user_areas ua
                ON ua.user_id=u.id
            INNER JOIN zones z
                ON z.zone_id=ua.zone_id
            WHERE role_id = 2 
            ORDER BY created_at DESC
            """
    admins = query_db(query)

    if not admins:
        return jsonify([])

    return jsonify(admins)

@admin_bp.route('/planners', methods=['GET'])
@token_required
def get_all_planners(current_user):

    user_id = current_user['id']
    user_role_id = current_user['role_id']

    if user_role_id == roles.get("SUPERADMIN"):
        query = """
            SELECT 
    u.id,
    u.first_name,
    u.last_name,
    u.email AS user_email,
    u.employee_id,
    u.created_at,
    z.zone_name,
    s.state_name,
    c.city_name,
    u.zone_id,
    u.state_id,
    u.city_id,
    cu.email AS created_by_user_email
FROM 
    users AS u 
    
INNER JOIN 
    zones AS z 
ON 
    z.zone_id = u.zone_id 

INNER JOIN 
    states AS s 
ON 
    s.state_id = u.state_id

INNER JOIN 
    cities AS c
ON 
    c.city_id = u.city_id 

LEFT JOIN 
    users AS cu 
ON 
    cu.id = u.created_by_user_id 
WHERE 
    u.role_id = 1 
ORDER BY 
    u.created_at DESC;

        """
        admins = query_db(query)

        if not admins:
            return jsonify([])

        return jsonify(admins)
    
    else:
        query = """
            SELECT 
    u.id,
    u.first_name,
    u.last_name,
    u.email AS user_email,
    u.created_at,
    z.zone_name,
    u.zone_id
FROM 
    users AS u 
INNER JOIN 
    zones AS z 
ON 
    z.zone_id = u.zone_id
WHERE 
    u.role_id = 1 
    AND 
    u.created_by_user_id=%s
ORDER BY 
    u.created_at DESC
        """
        admins = query_db(query, (user_id,))

        if not admins:
            return jsonify([])

        return jsonify(admins)

@admin_bp.route('/planners', methods=['POST'])
@token_required
def createPlanner(current_user):

    user_id = current_user['id']
    user_role_id = current_user['role_id']

    if user_role_id == roles.get("SUPERADMIN"):
        query = """
            SELECT 
    u.id,
    u.first_name,
    u.last_name,
    u.email AS user_email,
    u.employee_id,
    u.created_at,
    z.zone_name,
    s.state_name,
    c.city_name,
    u.zone_id,
    u.state_id,
    u.city_id,
    cu.email AS created_by_user_email
FROM 
    users AS u 
    
INNER JOIN 
    zones AS z 
ON 
    z.zone_id = u.zone_id 

INNER JOIN 
    states AS s 
ON 
    s.state_id = u.state_id

INNER JOIN 
    cities AS c
ON 
    c.city_id = u.city_id 

LEFT JOIN 
    users AS cu 
ON 
    cu.id = u.created_by_user_id 
WHERE 
    u.role_id = 1 
ORDER BY 
    u.created_at DESC;

        """
        admins = query_db(query)

        if not admins:
            return jsonify([])

        return jsonify(admins)
    
    else:
        query = """
            SELECT 
    u.id,
    u.first_name,
    u.last_name,
    u.email AS user_email,
    u.created_at,
    z.zone_name,
    u.zone_id
FROM 
    users AS u 
INNER JOIN 
    zones AS z 
ON 
    z.zone_id = u.zone_id
WHERE 
    u.role_id = 1 
    AND 
    u.created_by_user_id=%s
ORDER BY 
    u.created_at DESC
        """
        admins = query_db(query, (user_id,))

        if not admins:
            return jsonify([])

        return jsonify(admins)
    
@admin_bp.route('/admins', methods=['POST'])
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
    
    if data['zone_id'] == None or data['zone_id'] == '':
            return jsonify({'message': 'zone Id is required!'}), 400

    # if data['role_id'] == roles['PLANNER']:
    #     if data['state_id'] == None or data['state_id'] == '':
    #         return jsonify({'message': 'State Id is required!'}), 400
        
    #     if data['city_id'] == None or data['city_id'] == '':
    #         return jsonify({'message': 'city Id is required!'}), 400

    hashed_pass = generate_bcrypt_hash(data['password'])
    query = "INSERT INTO users (email, password, role_id, first_name, last_name, employee_id, created_by_user_id) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    args = (
        user_email, 
        hashed_pass,
        roles.get("ADMIN"), 
        clean_and_lower(data.get('first_name')), 
        clean_and_lower(data.get('last_name')), 
        user_emp_id,
        current_user_id
    )

    inserted_id = query_db(query, args, False, True)

    insert_user_areas(inserted_id, data['zone_id'])

    return jsonify({'message': 'User added successfully'}), 201

@admin_bp.route('/admins/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user,user_id):

    try:

        current_user_id = current_user['id']
        user_role_id = current_user['role_id']

        if user_role_id == roles.get("SUPERADMIN"):

            query = "DELETE FROM user_areas WHERE user_id = %s"
            args=(user_id,)
            query_db(query, args, False)

            query = "DELETE FROM users WHERE id = %s"
            args=(user_id,)
            query_db(query, args, False)

            query_db("COMMIT")

            return jsonify({'message': 'user deleted successfully'}), 200
        
        if user_role_id == roles.get("ADMIN"):
            # check if email exists!
            user_q = """
                SELECT * FROM users WHERE id=%s
            """
            ext_user = query_db(user_q, (user_id,), True)

            if ext_user == None:
                return jsonify({'message': 'User does not exist!'}), 400

            if ext_user['created_by_user_id'] != current_user_id:
                return jsonify({'message': 'You cannot delete this user!'}), 400
            

            query = "DELETE FROM user_areas WHERE user_id = %s"
            args=(user_id,)
            query_db(query, args, False)

            query = "DELETE FROM users WHERE id = %s"
            args=(user_id,)
            query_db(query, args, False)

            query_db("COMMIT")

            return jsonify({'message': 'user deleted successfully'}), 200
        
        return jsonify({'message': 'You dont have access!'}), 400

    except Exception as e:
        query_db("ROLLBACK")
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admins/<int:user_id>', methods=['PUT'])
@token_required
@superadmin_required
def update_user(current_user, user_id):
    try:
        data = request.get_json()

        zone_id = data['zone_id']

        if zone_id == None or zone_id == '':
            return jsonify({'message': 'zone Id is required!'}), 400
    
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

        user_area_q = """
            UPDATE user_areas
                SET zone_id=%s
            WHERE user_id=%s
        """
        query_db(user_area_q, (zone_id, user_id), False, True)

        return jsonify({'message': 'User updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

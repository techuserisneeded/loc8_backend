from flask import Blueprint, jsonify, request, current_app
from app.utils.helpers import token_required, superadmin_required, admin_required
from app.utils.db_helper import query_db
from app.utils.helpers import clean_and_lower, generate_bcrypt_hash
from app.constants.roles import roles
from app.services.users import is_user_email_exits, is_emp_id_exits
from app.services.user_areas import insert_user_areas

planners_bp = Blueprint('planners', __name__)

@planners_bp.route('/planner', methods=['POST'])
@token_required
@admin_required
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
        roles.get("PLANNER"), 
        clean_and_lower(data.get('first_name')), 
        clean_and_lower(data.get('last_name')), 
        user_emp_id,
        current_user_id
    )

    query_db(query, args, True, True)

    return jsonify({'message': 'User added successfully'}), 201


@planners_bp.route('/planners', methods=['GET'])
@token_required
@admin_required
def get_all_planners(current_user):
    query = """
        SELECT users.id, users.email, users.role_id,
               users.first_name, users.last_name, users.employee_id, 
               cu.email as created_by_user_email, users.created_at
        FROM `users`
        INNER JOIN users cu on users.id=cu.id 
        WHERE users.role_id = 1 order by users.created_at desc
        """
    planners = query_db(query)

    if not planners:
        planners = []

    data = []

    for planner in planners:
        q = """
                SELECT ua.*, z.zone_name, s.state_name, c.city_name FROM user_areas ua
                INNER JOIN zones z ON z.zone_id=ua.zone_id
                INNER JOIN states s ON s.state_id=ua.state_id
                INNER JOIN cities c ON c.city_id=ua.city_id
                WHERE 
                    user_id=%s
            """

        user_areas = query_db(q, (planner['id'],))

        if user_areas == None:
            user_areas = []

        planner["user_areas"] =  user_areas

        data.append(planner)

    return jsonify(data)

@planners_bp.route('/planners/<int:user_id>', methods=['PUT'])
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

@planners_bp.route('/planners/<int:user_id>/area_assign', methods=['PUT'])
@token_required
@admin_required
def assignAreas(current_user, user_id):
    
    data = request.get_json()

    for area in data:
        if not area['zone_id']:
            return jsonify({"message": "zone is required"}), 400
        
        if not area['state_id']:
            return jsonify({"message": "state is required"}), 400
        
        if not area['city_id']:
            return jsonify({"message": "city is required"}), 400    
        

    for area in data:
        q ="""
            SELECT * FROM user_areas
            WHERE zone_id=%s AND state_id=%s AND city_id=%s
        """
        args = (area['zone_id'], area['state_id'], area['city_id'])

        users = query_db(q, args)

        if users!=None and (len(users)>1 or user_id!= users[0]['user_id']):
            return jsonify({"message": "A Planner with this zone-state-city is already assigned!"}), 400
        
    try:
        query_db("START TRANSACTION")

        query_db("DELETE FROM user_areas WHERE user_id=%s", (user_id,))

        for area in data:
            insert_q = """
                INSERT INTO user_areas (user_id, zone_id, state_id, city_id)
                            VALUES (%s, %s, %s, %s)
            """

            query_db(insert_q, (user_id, area['zone_id'], area['state_id'], area['city_id']))


        query_db("COMMIT")

        return jsonify({'message': 'saved successfully!!'}), 200

    except Exception as e:
        print(e)
        query_db("ROLLBACK")
        return jsonify({'message': 'Something went wrong!'}), 500

        

        
        
        


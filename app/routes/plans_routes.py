import os
from flask import Blueprint, jsonify, request, current_app
from app.utils.helpers import token_required, superadmin_required, admin_required
from app.utils.db_helper import query_db
from werkzeug.utils import secure_filename
from app.utils.helpers import clean_and_lower, generate_bcrypt_hash, generate_uuid
from app.constants.roles import roles
from app.services.users import is_user_email_exits, is_emp_id_exits
from app.services.user_areas import insert_user_areas
from app.utils.helpers import generate_uuid

plans_bp = Blueprint('plans', __name__)

@plans_bp.route('/plans', methods=['POST'])
@token_required
def add_plan(current_user):

    current_user_id = current_user['id']

    data = request.form

    if 'map_image' not in request.files:
        return jsonify({'message': 'Map Image Is Required!'}), 400
    
    if 'site_image' not in request.files:
        return jsonify({'message': 'Site Image Is Required!'}), 400

    map_image_file = request.files['map_image']
    site_image_file = request.files['site_image']

    if map_image_file.filename == '':
        return jsonify({'message': 'Map Image Is Required!'}), 400
    
    if site_image_file.filename == '':
        return jsonify({'message': 'Site Image Is Required!'}), 400

    #data
    media_type = data['media_type']
    illumination = data['illumination']

    location = data['location']
    latitude = float(data['latitude'])
    longitude = float(data['longitude'])

    duration = float(data['duration'])
    imp_per_month =  float(data['imp_per_month'])
    mounting_rate = float(data['mounting'])
    printing_rate = float(data['printing'])
    rental_per_month = float(data['rental_per_month'])

    height = float(data['h'])
    width = float(data['w'])
    qty = int(data['qty'])
    size = float(data['size'])
    units = float(data['units'])
    
    brief_id = data['brief_id']
    budget_id = data['budget_id']
    video_id = data['video_id']

    cost_for_duration = (rental_per_month * duration) / 30

    plan_id = generate_uuid()

    map_img_filename = generate_uuid() + secure_filename(map_image_file.filename)
    site_img_filename = generate_uuid() + secure_filename(site_image_file.filename)

    query = """
        UPDATE billboards
        SET
            location=%s, 
            latitude=%s, 
            longitude=%s, 
            illumination=%s, 
            media_type=%s, 
            width=%s, 
            height=%s, 
            quantity=%s, 
            size=%s, 
            units=%s, 
            duration=%s, 
            imp_per_month=%s, 
            rental_per_month=%s, 
            printing_rate=%s, 
            mounting_rate=%s, 
            cost_for_duration=%s, 
            map_image=%s, 
            site_image=%s
        WHERE
            id=%s
    """

    args = (
        plan_id, brief_id, budget_id, 
        current_user_id, video_id, location, 
        latitude, longitude, illumination, 
        media_type, width, height, 
        qty, size, units, 
        duration, imp_per_month, rental_per_month, 
        printing_rate, mounting_rate, cost_for_duration, 
        map_img_filename, site_img_filename, billboard_id
    )

    query_db(query, args, True, True)

    map_image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], map_img_filename))
    site_image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], site_img_filename))

    return jsonify({'message': 'Plan added successfully'}), 201

      
@plans_bp.route('/plans/<plan_id>', methods=['DELETE'])
@token_required
def delete_plan_by_id(current_user, plan_id):
    query  = """
        DELETE FROM plans WHERE plan_id=%s
    """

    args=(plan_id,)

    query_db(query, args, False, True)

    return jsonify({'message': 'Plan deleted succesfully!'}), 200


@plans_bp.route('/plans/assets', methods=['POST'])
@token_required
def add_array_to_plan(current_user):

    current_user_id = current_user['id']

    data = request.get_json()

    billboards = data.get("billboards")
    budget_id = data.get("budget_id")
    brief_id = data.get("brief_id")
    video_id = data.get("video_id")
    
    try:
        query_db("START TRANSACTION")

        for bill_id in billboards:

            plan_id = generate_uuid()

            q = """
                INSERT INTO plans (plan_id, brief_id, budget_id, user_id, video_id, billboard_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            v = (plan_id, brief_id, budget_id, current_user_id, video_id, bill_id)

            query_db(q, v)

            query_db("COMMIT")

        return jsonify({'message': 'Plan added successfully'}), 201
        
    except Exception as e:
        print(str(e))
        query_db("ROLLBACK")

        return jsonify({'message': 'something went wrong!'}), 500


@plans_bp.route('/plans/media', methods=['GET'])
@token_required
def get_media_data(current_user):

    data = request.args

    city_id = data.get("city_id")
    state_id = data.get("state_id")
    zone_id = data.get("zone_id")

    q = """
        SELECT b.* FROM videofiles as v 
        INNER JOIN billboards b ON b.video_id=v.video_id
        WHERE v.zone_id=%s AND v.state_id=%s AND v.city_id=%s 
    """

    values = (zone_id, state_id, city_id)

    billboards = query_db(q, values)

    return jsonify(billboards), 200


    
   



    



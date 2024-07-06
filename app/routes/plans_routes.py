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
    
    last_plan = query_db("""
                    SELECT sr_no 
                    FROM plans 
                    WHERE 
                        brief_id=%s AND budget_id=%s AND user_id=%s 
                    ORDER BY sr_no 
                    DESC 
                    LIMIT 1
                """, 
                (brief_id, budget_id, current_user_id),
                True
                )

    last_plan_sr_no = last_plan.get("sr_no") if last_plan != None else 0 
    
    try:
        query_db("START TRANSACTION")

        for bill_id in billboards:

            plan_id = generate_uuid()
            
            last_plan_sr_no = last_plan_sr_no + 1   

            q = """
                INSERT INTO plans (plan_id, brief_id, budget_id, user_id, sr_no, billboard_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            v = (plan_id, brief_id, budget_id, current_user_id, last_plan_sr_no, bill_id)

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
    grouped_data = {}
    
    for key, value in data.items():
    # Extract the prefix (0, 1, 2, etc.)
        prefix = key.split('[')[0]
        if prefix == '0' or prefix == '1' or prefix == '2' or prefix == '3':
        # Initialize a list for the prefix if it doesn't exist
            if prefix not in grouped_data:
                grouped_data[prefix] = []
            
            # Append the value to the list corresponding to the prefix
            grouped_data[prefix].append(value)

# Convert the grouped data to a list of lists
    result = [grouped_data[key] for key in sorted(grouped_data.keys())]

# Print the result
    vendor_name = result[0]
    location = result[1]
    media_type = result[2]
    illumination = result[3]
    
    print(vendor_name, len(location), media_type, len(illumination))
    
    city_id = data.get("city_id")
    state_id = data.get("state_id")
    zone_id = data.get("zone_id")

    visibility_duration_min = float(data.get("visibility_duration_min", 0) or 0)
    visibility_duration_max = float(data.get("visibility_duration_max", 99999) or 99999)
    
    average_areas_min = float(data.get("average_areas_min", 0) or 0)
    average_areas_max = float(data.get("average_areas_max", 99999) or 99999)

    # near_p_duration_min = float(data.get("near_p_duration_min", 0) or 0)
    # near_p_duration_max = float(data.get("near_p_duration_max", 99999) or 99999)

    # mid_p_duration_min = float(data.get("mid_p_duration_min", 0) or 0)
    # mid_p_duration_max = float(data.get("mid_p_duration_max", 99999) or 99999)

    # far_p_duration_min = float(data.get("far_p_duration_min", 0) or 0)
    # far_p_duration_max = float(data.get("far_p_duration_max", 99999) or 99999)

    # distance_to_center_min = float(data.get("distance_to_center_min", 0) or 0)
    # distance_to_center_max = float(data.get("distance_to_center_max", 99999) or 99999)

    # near_p_distance_min = float(data.get("near_p_distance_min", 0) or 0)
    # near_p_distance_max = float(data.get("near_p_distance_max", 99999) or 99999)

    # mid_p_distance_min = float(data.get("mid_p_distance_min", 0) or 0)
    # mid_p_distance_max = float(data.get("mid_p_distance_max", 99999) or 99999)

    # far_p_distance_min = float(data.get("far_p_distance_min", 0) or 0)
    # far_p_distance_max = float(data.get("far_p_distance_max", 99999) or 99999)
    
    average_speed_min = float(data.get("average_speed_min", 0) or 0)
    average_speed_max = float(data.get("average_speed_max", 99999) or 99999)

    # length_of_stretch_min = float(data.get("length_of_stretch_min", 0) or 0)
    # length_of_stretch_max = float(data.get("length_of_stretch_max", 99999) or 99999)
    
    area_min = float(data.get("area_min", 0) or 0)
    area_max = float(data.get("area_max", 99999999) or 99999999)

    display_cost_per_month_min = float(data.get("display_cost_per_month_min", 0) or 0)
    display_cost_per_month_max = float(data.get("display_cost_per_month_max", 99999999) or 99999999)

    total_cost_min = float(data.get("total_cost_min", 0) or 0)
    total_cost_max = float(data.get("total_cost_max", 99999999) or 99999999)

    front_saliency_score_city_min = float(data.get("front_saliency_score_city_min", 0) or 0)
    front_saliency_score_city_max = float(data.get("front_saliency_score_city_max", 101) or 101)

    rear_saliency_score_city_min = float(data.get("rear_saliency_score_city_min", 0) or 0)
    rear_saliency_score_city_max = float(data.get("rear_saliency_score_city_max", 101) or 101)

    net_saliency_score_city_min = float(data.get("net_saliency_score_city_min", 0) or 0)
    net_saliency_score_city_max = float(data.get("net_saliency_score_city_max", 101) or 101)


    impressions_min = float(data.get("impressions_min", 0) or 0)
    impressions_max = float(data.get("impressions_max", 1000000000) or 1000000000)

    effective_impressions_min = float(data.get("effective_impressions_min", 0) or 0)
    effective_impressions_max = float(data.get("effective_impressions_max", 1000000000) or 1000000000)

    efficiency_min = float(data.get("efficiency_min", 0) or 0)
    efficiency_max = float(data.get("efficiency_max", 10000000) or 10000000)
    top_impressions = int(data.get("top_impressions", 1000000) or 1000000)
    top_area = int(data.get("top_area", 100000) or 10000)
    top_average_speed = int(data.get("top_average_speed", 100000) or 10000)
    top_display_cost_per_month = int(data.get("top_display_cost_per_month", 100000) or 10000)
    top_total_cost = int(data.get("top_total_cost", 100000) or 10000)
    top_visibility_duration = int(data.get("top_visibility_duration", 100000) or 10000)
    top_front_saliency_citywise = int(data.get("top_front_saliency_citywise", 100000) or 10000)
    top_rear_saliency_citywise = int(data.get("top_rear_saliency_citywise", 100000) or 10000)
    top_net_saliency_citywise = int(data.get("top_net_saliency_citywise", 100000) or 10000)
    top_front_saliency_locationwise = int(data.get("top_front_saliency_locationwise", 100000) or 10000)
    top_rear_saliency_locationwise = int(data.get("top_rear_saliency_locationwise", 100000) or 10000)
    top_net_saliency_locationwise = int(data.get("top_net_saliency_locationwise", 100000) or 10000)
    top_effective_impressions = int(data.get("top_effective_impressions", 100000) or 10000)
    top_efficiency = int(data.get("top_efficiency", 100000) or 10000)

    # if location is not None:
        # q = """
        #     SELECT b.* FROM videofiles as v 
        #     INNER JOIN billboards b ON b.video_id=v.video_id
        #     WHERE v.zone_id=%s 
        #     AND v.state_id=%s 
        #     AND v.city_id=%s
        #     AND visibility_duration>=%s 
        #     AND visibility_duration<=%s
        #     AND average_speed>=%s 
        #     AND average_speed<=%s
        #     AND display_cost_per_month>=%s 
        #     AND display_cost_per_month<=%s
        #     AND total_cost>=%s
        #     AND total_cost<=%s
        #     AND saliency_score_front_city>=%s
        #     AND saliency_score_front_city<=%s
        #     AND saliency_score_rear_city>=%s
        #     AND saliency_score_rear_city<=%s
        #     AND net_saliency_score_city>=%s
        #     AND net_saliency_score_city<=%s
        #     AND effective_impression>=%s
        #     AND effective_impression<=%s
        #     AND area>=%s 
        #     AND area<=%s
        #     AND (location LIKE CONCAT('%%' ,%s, '%%')
        #     OR location LIKE CONCAT(%s, '%%')
        #     OR location LIKE CONCAT('%%' ,%s)
        #     OR location = %s);
        # """
        
    q = """WITH ranked_billboards AS (
    SELECT b.*, v.zone_id, v.state_id, v.city_id, v.average_speed,
        ROW_NUMBER() OVER (ORDER BY area DESC) AS rank_area,
        ROW_NUMBER() OVER (ORDER BY display_cost_per_month DESC) AS rank_display_cost_per_month,
        ROW_NUMBER() OVER (ORDER BY visibility_duration DESC) AS rank_visibility_duration,
        ROW_NUMBER() OVER (ORDER BY total_cost DESC) AS rank_total_cost,
        ROW_NUMBER() OVER (ORDER BY effective_impression DESC) AS rank_effective_impression,
        ROW_NUMBER() OVER (ORDER BY efficiency DESC) AS rank_efficiency
    FROM
        videofiles as v INNER JOIN billboards b on b.video_id = v.video_id 
)
SELECT *
FROM ranked_billboards rb
WHERE 
    rb.zone_id = %s
    AND rb.state_id = %s 
    AND rb.city_id = %s 
    AND rb.visibility_duration >= %s
    AND rb.visibility_duration <= %s
    AND rb.average_speed>=%s
    AND rb.average_speed<=%s 
    AND rb.display_cost_per_month>=%s 
    AND rb.display_cost_per_month<=%s
    AND rb.total_cost>=%s
    AND rb.total_cost<=%s
    AND rb.saliency_score_front_city>=%s
    AND rb.saliency_score_front_city<=%s
    AND rb.saliency_score_rear_city>=%s
    AND rb.saliency_score_rear_city<=%s
    AND rb.net_saliency_score_city>=%s
    AND rb.net_saliency_score_city<=%s
    AND rb.effective_impression>=%s
    AND rb.effective_impression<=%s
    AND rb.area>=%s 
    AND rb.area<=%s
    AND rb.rank_front_saliency_citywise <= %s
    AND rb.rank_rear_saliency_citywise <= %s
    AND rb.rank_net_saliency_citywise <= %s
    AND rank_saliency_front_locationwise <= %s
    AND rank_saliency_rear_locationwise <= %s
    AND rank_net_saliency_locationwise <= %s
    AND (rank_area <= %s OR %s IS NULL) 
    AND (rank_display_cost_per_month <= %s OR %s IS NULL)
    AND (rank_visibility_duration <= %s OR %s IS NULL)
    AND (rank_total_cost <= %s OR %s IS NULL)
    AND (rank_effective_impression <= %s OR %s IS NULL)
    AND (rank_efficiency <= %s OR %s IS NULL)
    """
    
    
    like_conditions = []
    for name in vendor_name:
        if name != '':
            like_conditions.append(f"rb.vendor_name LIKE '%%{name}%%'")

    # Join all LIKE conditions with OR
    if like_conditions:
        q += " AND (" + " OR ".join(like_conditions) + ")"
            
    like_conditions = []
    for single_location in location:
        if single_location!='':
            like_conditions.append(f"rb.location LIKE '%%{single_location}%%'")

    # Join all LIKE conditions with OR
    if like_conditions:
        q += " AND (" + " OR ".join(like_conditions) + ")"
        
    like_conditions = []
    for single_media_type in media_type:
        if single_media_type!='':
            like_conditions.append(f"rb.media_type LIKE '%%{single_media_type}%%'")

    # Join all LIKE conditions with OR
    if like_conditions:
        q += " AND (" + " OR ".join(like_conditions) + ")"
    
    like_conditions = []
    for illum in illumination:
        if illum != '':
            like_conditions.append(f"rb.illumination LIKE '%%{illum}%%'")
    # Join all LIKE conditions with OR
    if like_conditions:
        q += " AND (" + " OR ".join(like_conditions) + ")"
        
        
    q += """
    ORDER BY area DESC, display_cost_per_month DESC, visibility_duration DESC, total_cost DESC, effective_impression DESC, efficiency DESC
    """
        
        
    values = (
        zone_id, state_id, city_id, visibility_duration_min, visibility_duration_max,
        average_speed_min, average_speed_max, display_cost_per_month_min, display_cost_per_month_max,
        total_cost_min, total_cost_max, front_saliency_score_city_min, front_saliency_score_city_max, rear_saliency_score_city_min, 
        rear_saliency_score_city_max, net_saliency_score_city_min, net_saliency_score_city_max,
        effective_impressions_min, effective_impressions_max, area_min, area_max,
        top_front_saliency_citywise, top_rear_saliency_citywise, top_net_saliency_citywise,top_front_saliency_locationwise, top_rear_saliency_locationwise
        ,top_net_saliency_locationwise,top_area, top_area, top_display_cost_per_month, top_display_cost_per_month, top_visibility_duration, top_visibility_duration, 
        top_total_cost, top_total_cost, top_effective_impressions, top_effective_impressions, top_efficiency, top_efficiency
    )

    billboards = query_db(q, values)
    return jsonify(billboards), 200

# else:
    #     q = """
    #             SELECT b.* FROM videofiles as v 
    #         INNER JOIN billboards b ON b.video_id=v.video_id
    #         WHERE v.zone_id=%s 
    #         AND v.state_id=%s 
    #         AND v.city_id=%s
    #         AND visibility_duration>=%s 
    #         AND visibility_duration<=%s
    #         AND average_speed>=%s 
    #         AND average_speed<=%s
    #         AND display_cost_per_month>=%s 
    #         AND display_cost_per_month<=%s
    #         AND total_cost>=%s
    #         AND total_cost<=%s
    #         AND saliency_score_front_city>=%s
    #         AND saliency_score_front_city<=%s
    #         AND saliency_score_rear_city>=%s
    #         AND saliency_score_rear_city<=%s
    #         AND net_saliency_score_city>=%s
    #         AND net_saliency_score_city<=%s
    #         AND effective_impression>=%s
    #         AND effective_impression<=%s
    #         AND area>=%s 
    #         AND area<=%s
            
    #         """
    #     values = (
    #             zone_id, state_id, city_id, 
    #         visibility_duration_min, visibility_duration_max,
    #         average_speed_min, average_speed_max,
    #         display_cost_per_month_min, display_cost_per_month_max,
    #         total_cost_min, total_cost_max, front_saliency_score_city_min, front_saliency_score_city_max,
    #         rear_saliency_score_city_min, rear_saliency_score_city_max, net_saliency_score_city_min,
    #         net_saliency_score_city_max,effective_impressions_min, effective_impressions_max,
    #         area_min, area_max)

    #     billboards = query_db(q, values)

    #     return jsonify(billboards), 200

    



        



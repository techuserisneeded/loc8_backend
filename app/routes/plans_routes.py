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
    
        prefix = key.split('[')[0]
        if prefix == '0' or prefix == '1' or prefix == '2' or prefix == '3':
      
            if prefix not in grouped_data:
                grouped_data[prefix] = []
            
    
            grouped_data[prefix].append(value)


    result = [grouped_data[key] for key in sorted(grouped_data.keys())]


    vendor_name = result[0]
    location = result[1]
    media_type = result[2]
    illumination = result[3]
    

    
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
    top_area = int(data.get("top_area", 100000) or 100000)
    
    top_average_speed = int(data.get("top_average_speed", 100000) or 100000)
    
    
    top_display_cost_per_month = int(data.get("top_display_cost_per_month", 100000) or 100000)
    
    
    top_total_cost = int(data.get("top_total_cost", 100000) or 100000)
    top_visibility_duration = int(data.get("top_visibility_duration", 100000) or 100000)
    top_front_saliency_citywise = int(data.get("top_front_saliency_citywise", 100000) or 100000)
    top_rear_saliency_citywise = int(data.get("top_rear_saliency_citywise", 100000) or 100000)
    top_net_saliency_citywise = int(data.get("top_net_saliency_citywise", 100000) or 100000)
    top_front_saliency_locationwise = int(data.get("top_front_saliency_locationwise", 100000) or 100000)
    top_rear_saliency_locationwise = int(data.get("top_rear_saliency_locationwise", 100000) or 100000)
    top_net_saliency_locationwise = int(data.get("top_net_saliency_locationwise", 100000) or 100000)
    top_effective_impressions = int(data.get("top_effective_impressions", 100000) or 100000)
    top_efficiency = int(data.get("top_efficiency", 100000) or 100000)
    top_impressions = int(data.get("top_impressions", 100000) or 100000)

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
    qq = """WITH city_filtered AS (
    SELECT b.*, v.zone_id, v.state_id, v.city_id, v.average_speed
    FROM videofiles v
    INNER JOIN billboards b ON b.video_id = v.video_id
    WHERE v.zone_id = %s
        AND v.state_id = %s
        AND v.city_id = %s
        AND visibility_duration >= %s
        AND visibility_duration <= %s
        AND v.average_speed >= %s
        AND v.average_speed <= %s 
        AND display_cost_per_month >= %s 
        AND display_cost_per_month <= %s
        AND area >= %s 
        AND area <= %s"""
    q = """
ranked_billboards AS (
    SELECT *,
        ROW_NUMBER() OVER (ORDER BY saliency_score_front_city DESC) AS rank_saliency_front_citywise,
        ROW_NUMBER() OVER (ORDER BY saliency_score_rear_city DESC) AS rank_saliency_rear_citywise,
        ROW_NUMBER() OVER (ORDER BY net_saliency_score_city DESC) AS rank_saliency_net_citywise,
        ROW_NUMBER() OVER (ORDER BY area DESC) AS rank_area,
        ROW_NUMBER() OVER (ORDER BY rental_per_month DESC) AS rank_display_cost_per_month,
        ROW_NUMBER() OVER (ORDER BY visibility_duration DESC) AS rank_visibility_duration,
        ROW_NUMBER() OVER (ORDER BY effective_impression DESC) AS rank_effective_impression,
        ROW_NUMBER() OVER (ORDER BY efficiency DESC) AS rank_efficiency,
        ROW_NUMBER() OVER (ORDER BY impression DESC) AS rank_impressions
    FROM city_filtered
)
SELECT *
FROM ranked_billboards rb
WHERE 
    (rb.rank_saliency_front_citywise <= %s OR %s IS NULL) 
    AND (rb.rank_saliency_rear_citywise <= %s OR %s IS NULL) 
    AND (rb.rank_saliency_net_citywise <= %s OR %s IS NULL) 
    AND (rb.rank_area <= %s OR %s IS NULL) 
    AND (rb.rank_display_cost_per_month <= %s OR %s IS NULL)
    AND (rb.rank_visibility_duration <= %s OR %s IS NULL)
    AND (rb.rank_effective_impression <= %s OR %s IS NULL)
    AND (rb.rank_efficiency <= %s OR %s IS NULL)
    AND (rb.rank_impressions <= %s OR %s IS NULL)
    """
    like_conditions = []
    for name in vendor_name:
        if name != '':
            like_conditions.append(f"vendor_name LIKE '%%{name}%%'")

    # Join all LIKE conditions with OR
    if like_conditions:
        qq += " AND (" + " OR ".join(like_conditions) + ")"
            
    like_conditions = []
    for single_location in location:
        if single_location!='':
            like_conditions.append(f"location LIKE '%%{single_location}%%'")

    # Join all LIKE conditions with OR
    if like_conditions:
        qq += " AND (" + " OR ".join(like_conditions) + ")"
        
    like_conditions = []
    for single_media_type in media_type:
        if single_media_type!='':
            like_conditions.append(f"media_type LIKE '%%{single_media_type}%%'")

    # Join all LIKE conditions with OR
    if like_conditions:
        qq += " AND (" + " OR ".join(like_conditions) + ")"
    
    like_conditions = []
    for illum in illumination:
        if illum != '':
            like_conditions.append(f"illumination LIKE '%%{illum}%%'")
    # Join all LIKE conditions with OR
    if like_conditions:
        qq += " AND (" + " OR ".join(like_conditions) + ")"
        
    qq += '''),'''
    q += """
    ORDER BY saliency_score_front_city DESC, saliency_score_front_city DESC, net_saliency_score_city DESC, area DESC, rental_per_month DESC, visibility_duration DESC, total_cost DESC, effective_impression DESC, efficiency DESC, impression DESC
    """
    qq += q
    # print("Query", qq)
    values = (
        zone_id, state_id, city_id, visibility_duration_min, visibility_duration_max,
        average_speed_min, average_speed_max, display_cost_per_month_min, display_cost_per_month_max, area_min, area_max,
        top_front_saliency_citywise,top_front_saliency_citywise, top_rear_saliency_citywise, top_rear_saliency_citywise, top_net_saliency_citywise,top_net_saliency_citywise,top_area, top_area, top_display_cost_per_month, top_display_cost_per_month, top_visibility_duration, top_visibility_duration, top_effective_impressions, top_effective_impressions, top_efficiency, 
        top_efficiency, top_impressions, top_impressions
    )
    billboards = query_db(qq, values)
    
    
    
    
    temp = '''CREATE TEMPORARY TABLE temp_filtered_billboards (
  id varchar(36) NOT NULL,
  video_id varchar(36) DEFAULT NULL,
  visibility_duration float DEFAULT NULL,
  distance_to_center float DEFAULT NULL,
  central_duration float DEFAULT NULL,
  near_p_duration float DEFAULT NULL,
  mid_p_duration float DEFAULT NULL,
  far_p_duration float DEFAULT NULL,
  central_distance float DEFAULT NULL,
  near_p_distance float DEFAULT NULL,
  mid_p_distance float DEFAULT NULL,
  far_p_distance float DEFAULT NULL,
  average_areas float DEFAULT NULL,
  confidence float DEFAULT NULL,
  tracker_id int(11) DEFAULT NULL,
  created_at timestamp NOT NULL DEFAULT current_timestamp(),
  created_by_user_id int(11) NOT NULL,
  latitude decimal(9,6) DEFAULT NULL,
  longitude decimal(9,6) DEFAULT NULL,
  vendor_name varchar(255) DEFAULT NULL,
  location varchar(255) DEFAULT NULL,
  traffic_direction varchar(255) DEFAULT NULL,
  media_type varchar(255) DEFAULT NULL,
  illumination varchar(255) DEFAULT NULL,
  width float DEFAULT 0,
  height float DEFAULT 0,
  quantity float DEFAULT 0,
  area float DEFAULT 0,
  display_cost_per_month float DEFAULT 0,
  printing_rate float DEFAULT 0,
  mounting_rate float DEFAULT 0,
  printing_cost decimal(10,2) DEFAULT NULL,
  mounting_cost decimal(10,2) DEFAULT NULL,
  total_cost decimal(10,2) DEFAULT NULL,
  site_image varchar(255) DEFAULT NULL,
  map_image varchar(255) DEFAULT NULL,
  focal_vision_duration float DEFAULT 0,
  saliency_score_front_city float DEFAULT NULL,
  saliency_score_rear_city float DEFAULT 0,
  net_saliency_score_city float DEFAULT 0,
  duration int(11) DEFAULT 0,
  rental_per_month float DEFAULT 0,
  cost_for_duration decimal(10,2) DEFAULT NULL,
  Rank_net_saliency_citywise int(11) NOT NULL DEFAULT 0,
  rank_saliency_front_locationwise int(11) NOT NULL DEFAULT 0,
  rank_saliency_rear_locationwise int(11) NOT NULL DEFAULT 0,
  rank_net_saliency_locationwise int(11) NOT NULL DEFAULT 0,
  Rank_front_saliency_citywise int(11) NOT NULL DEFAULT 0,
  Rank_rear_saliency_citywise int(11) NOT NULL DEFAULT 0,
  efficiency float NOT NULL DEFAULT 0,
  impression_id int(11) DEFAULT NULL,
  effective_impression decimal(15,4) NOT NULL DEFAULT 0.0000,
  
  zone_id int(11) DEFAULT NULL,
  state_id int(11) DEFAULT NULL,
  city_id int(11) DEFAULT NULL,
  average_speed float DEFAULT NULL,
 rank_saliency_front_citywise int(11) NOT NULL DEFAULT 0, 
rank_saliency_rear_citywise int(11) NOT NULL DEFAULT 0, 
rank_saliency_net_citywise int(11) NOT NULL DEFAULT 0, 
rank_area int(11) NOT NULL DEFAULT 0,
 rank_display_cost_per_month int(11) NOT NULL DEFAULT 0, 
rank_visibility_duration int(11) NOT NULL DEFAULT 0,
 rank_effective_impression int(11) NOT NULL DEFAULT 0, 
rank_efficiency int(11) NOT NULL DEFAULT 0,
rank_impressions int(11) NOT NULL DEFAULT 0,
impression int(11) DEFAULT NULL
);
'''
    query_db(temp)


    if billboards is not None:
        
        for billboard in billboards:        
            temp = '''INSERT INTO temp_filtered_billboards (
                id, video_id, visibility_duration, distance_to_center, central_duration, near_p_duration, 
                mid_p_duration, far_p_duration, central_distance, near_p_distance, mid_p_distance, 
                far_p_distance, average_areas, confidence, tracker_id, created_at, created_by_user_id, 
                latitude, longitude, vendor_name, location, traffic_direction, media_type, illumination, 
                width, height, quantity, area, display_cost_per_month, printing_rate, mounting_rate, 
                printing_cost, mounting_cost, total_cost, site_image, map_image, focal_vision_duration, 
                saliency_score_front_city, saliency_score_rear_city, net_saliency_score_city, duration, 
                rental_per_month, cost_for_duration, Rank_net_saliency_citywise, rank_saliency_front_locationwise, 
                rank_saliency_rear_locationwise, rank_net_saliency_locationwise, Rank_front_saliency_citywise, 
                Rank_rear_saliency_citywise, efficiency, impression_id, effective_impression, zone_id, state_id ,
    city_id , average_speed, rank_saliency_front_citywise, rank_saliency_rear_citywise, 
    rank_saliency_net_citywise, rank_area,rank_display_cost_per_month, 
    rank_visibility_duration, rank_effective_impression, rank_efficiency, rank_impressions, impression 
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s);
            '''
            values = (
                billboard['id'], billboard['video_id'], billboard['visibility_duration'], billboard['distance_to_center'],
                billboard['central_duration'], billboard['near_p_duration'], billboard['mid_p_duration'], 
                billboard['far_p_duration'], billboard['central_distance'], billboard['near_p_distance'], 
                billboard['mid_p_distance'], billboard['far_p_distance'], billboard['average_areas'], 
                billboard['confidence'], billboard['tracker_id'], billboard['created_at'], billboard['created_by_user_id'], 
                billboard['latitude'], billboard['longitude'], billboard['vendor_name'], billboard['location'], 
                billboard['traffic_direction'], billboard['media_type'], billboard['illumination'], billboard['width'], 
                billboard['height'], billboard['quantity'], billboard['area'], billboard['display_cost_per_month'], 
                billboard['printing_rate'], billboard['mounting_rate'], billboard['printing_cost'], billboard['mounting_cost'], 
                billboard['total_cost'], billboard['site_image'], billboard['map_image'], billboard['focal_vision_duration'], 
                billboard['saliency_score_front_city'], billboard['saliency_score_rear_city'], billboard['net_saliency_score_city'], 
                billboard['duration'], billboard['rental_per_month'], billboard['cost_for_duration'], 
                billboard['Rank_net_saliency_citywise'], billboard['rank_saliency_front_locationwise'], 
                billboard['rank_saliency_rear_locationwise'], billboard['rank_net_saliency_locationwise'], 
                billboard['Rank_front_saliency_citywise'], billboard['Rank_rear_saliency_citywise'], billboard['efficiency'], 
                billboard['impression_id'], billboard['effective_impression'], billboard['zone_id'], billboard['state_id'], billboard['city_id'],
                billboard['average_speed'], billboard['rank_saliency_front_citywise'], billboard['rank_saliency_rear_citywise'], 
    billboard['rank_saliency_net_citywise'], billboard['rank_area'],billboard['rank_display_cost_per_month'], 
    billboard['rank_visibility_duration'], billboard['rank_effective_impression'], billboard['rank_efficiency'], billboard['rank_impressions'], billboard['impression'] 
            )
            query_db(temp, values)
        
        
        
        billoards_q = """
                            SELECT DISTINCT
                        CASE
                            WHEN b.location IS NULL THEN NULL
                            WHEN INSTR(b.location, ',') > 0 THEN LEFT(b.location, INSTR(b.location, ',') - 1)
                            ELSE b.location
                        END AS location
                    FROM temp_filtered_billboards AS b
                """
        billboards = query_db(billoards_q)
        
      
        for bill in billboards: 
            unique_location = bill.get('location')
            if unique_location != None:

                ##Rank rear saliency locationwise
                billoards_q = """
                        Select
                        b.id,b.location, b.saliency_score_rear_city, RANK()
                        OVER ( ORDER BY saliency_score_rear_city DESC) as rank_saliency_rear_locationwise 
                        FROM temp_filtered_billboards as b 
                        WHERE 
                        CASE
                        WHEN INSTR(b.location, ',') > 0 THEN LEFT(b.location, INSTR(b.location, ',') - 1)
                        ELSE b.location
                    END = %s; 
                        """
                resultant = query_db(billoards_q, (unique_location,))
                if resultant is not None:
                    for res in resultant:
                        res_id = res.get('id')
                        q = """
                        UPDATE temp_filtered_billboards 
                        SET 
                            rank_saliency_rear_locationwise=%s
                        WHERE
                            id=%s
                        """
                        query_db(q, (res.get('rank_saliency_rear_locationwise'),res_id))
                    query_db("COMMIT")

                ##Rank front saliency locationwise
                billoards_q = """
                        Select
                        b.id,b.location, b.saliency_score_front_city, RANK()
                        OVER ( ORDER BY saliency_score_front_city DESC) as rank_saliency_front_locationwise 
                        FROM temp_filtered_billboards as b
                        WHERE
                        CASE
                        WHEN INSTR(b.location, ',') > 0 THEN LEFT(b.location, INSTR(b.location, ',') - 1)
                        ELSE b.location
                    END = %s; 
                        """
                resultant = query_db(billoards_q, (unique_location,))

                for res in resultant:
                    res_id = res.get("id")
                    q = """
                    UPDATE temp_filtered_billboards 
                    SET 
                        rank_saliency_front_locationwise=%s
                    WHERE
                        id=%s
                    """
                    query_db(q, (res.get('rank_saliency_front_locationwise'),res_id))
                query_db("COMMIT")

            ##Ranking Net saliency locationwise
                billoards_q = """
                            Select
                            b.id, b.location, b.net_saliency_score_city, RANK()
                            OVER ( ORDER BY net_saliency_score_city DESC) as rank_net_saliency_locationwise 
                            FROM temp_filtered_billboards as b
                            WHERE
                            CASE
                        WHEN INSTR(b.location, ',') > 0 THEN LEFT(b.location, INSTR(b.location, ',') - 1)
                        ELSE b.location
                            END = %s;   
                            """
                resultant = query_db(billoards_q, (unique_location,))

                for res in resultant:
                    res_id = res.get("id")
                    q = """
                    UPDATE temp_filtered_billboards
                    SET 
                        rank_net_saliency_locationwise=%s
                    WHERE
                        id=%s
                    """
                    query_db(q, (res.get('rank_net_saliency_locationwise'),res_id))
            query_db("COMMIT")
            
            
        
        final_q = '''
        Select * 
        from temp_filtered_billboards
        where (rank_net_saliency_locationwise <= %s or %s is NULL)
        AND
        (rank_saliency_front_locationwise <= %s or %s is NULL)
        AND
        (rank_saliency_rear_locationwise <= %s or %s is NULL)
        '''
        
        billboards = query_db(final_q, (top_net_saliency_locationwise, top_net_saliency_locationwise, top_front_saliency_locationwise, top_front_saliency_locationwise, top_rear_saliency_locationwise, top_rear_saliency_locationwise))
        print(billboards)

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

    



        



import os
from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename

from app.utils.helpers import token_required, superadmin_required, admin_required
from app.utils.db_helper import query_db
import app.utils.metrics as metrics
from app.utils.helpers import clean_and_lower, generate_bcrypt_hash, generate_uuid

from app.constants.roles import roles
from app.services.users import is_user_email_exits, is_emp_id_exits
from app.services.user_areas import insert_user_areas
from app.constants.default_weights import default_weights_front, default_weights_rear

metrics_bp = Blueprint('metrics', __name__)

@metrics_bp.route('/efficiency', methods=['POST'])
@token_required
def calculate_efficiency(current_user):

    billoards_q = """
            SELECT b.net_saliency_score_city, b.rental_per_month, b.id
            FROM billboards as b 
    """
    billboards = query_db(billoards_q)

    query_db("START TRANSACTION")

    for bill in billboards:
        bill_id = bill.get("id")
        efficiency = metrics.calculate_efficiency(bill.get("net_saliency_score_city"), bill.get("rental_per_month"))
        q = """
            UPDATE billboards 
            SET 
                efficiency = %s
            WHERE 
            id = %s
        """
        query_db(q, (efficiency, bill_id))
    query_db("COMMIT")

    return jsonify({'message': 'Efficiency calculated successfully'}), 201



@metrics_bp.route('/saliency', methods=['POST'])
@token_required
def calculate_saliency(current_user):

    body = request.get_json()

    zone_id = body.get("zone_id")
    state_id = body.get("state_id")
    city_id = body.get("city_id")
    level = body.get("level", "city")

    body_weights_front = body.get("front_weightings", {})
    body_weights_rear = body.get("rear_weightings", {})

    weights_front = {
        "distance_to_center": body_weights_front.get("distance_to_center", default_weights_front.get("distance_to_center")),
        "average_areas": body_weights_front.get("average_areas", default_weights_front.get("average_areas")),
        "focal_vision_duration": body_weights_front.get("focal_vision_duration", default_weights_front.get("focal_vision_duration")),
        "near_p_duration": body_weights_front.get("near_p_duration", default_weights_front.get("near_p_duration")),
        "mid_p_duration": body_weights_front.get("mid_p_duration", default_weights_front.get("mid_p_duration")),
        "far_p_duration": body_weights_front.get("far_p_duration", default_weights_front.get("far_p_duration")),
        "average_speed": body_weights_front.get("average_speed", default_weights_front.get("average_speed")),
    }

    weights_rear = {
        "distance_to_center": body_weights_rear.get("distance_to_center", default_weights_rear.get("distance_to_center")),
        "average_areas": body_weights_rear.get("average_areas", default_weights_rear.get("average_areas")),
        "focal_vision_duration": body_weights_rear.get("focal_vision_duration", default_weights_rear.get("focal_vision_duration")),
        "near_p_duration": body_weights_rear.get("near_p_duration", default_weights_rear.get("near_p_duration")),
        "mid_p_duration": body_weights_rear.get("mid_p_duration", default_weights_rear.get("mid_p_duration")),
        "far_p_duration": body_weights_rear.get("far_p_duration", default_weights_rear.get("far_p_duration")),
        "average_speed": body_weights_rear.get("average_speed", default_weights_rear.get("average_speed")),
    }

    billoards_q = """
            SELECT 
                b.id, b.video_id, b.distance_to_center, b.average_areas, b.focal_vision_duration,
                b.near_p_duration, b.mid_p_duration, b.far_p_duration, v.average_speed 
            FROM billboards as b INNER JOIN videofiles as v on v.video_id=b.video_id
            WHERE
                v.city_id=%s
    """

    billboards = query_db(billoards_q, (city_id,))

    query_db("START TRANSACTION")

    for bill in billboards:
        bill_id = bill.get("id")

        distance_to_center_front = metrics.calculate_distance_to_center(bill.get("distance_to_center"), weights_front.get("distance_to_center"))
        average_areas_front = metrics.calculate_average_areas(bill.get("average_areas"), weights_front.get("average_areas"))
        focal_vision_duration_front = metrics.calculate_focal_vision_duration(bill.get("focal_vision_duration"), weights_front.get("focal_vision_duration"))
        near_p_duration_front = metrics.calculate_near_p_duration(bill.get("near_p_duration"), weights_front.get("near_p_duration"))
        mid_p_duration_front = metrics.calculate_mid_p_duration(bill.get("mid_p_duration"), weights_front.get("mid_p_duration"))
        far_p_duration_front = metrics.calculate_far_p_duration(bill.get("far_p_duration"), weights_front.get("far_p_duration"))
        average_speed_front = metrics.calculate_average_speed(bill.get("average_speed"), weights_front.get("average_speed"))

        distance_to_center_rear = metrics.calculate_distance_to_center(bill.get("distance_to_center"), weights_rear.get("distance_to_center"))
        average_areas_rear = metrics.calculate_average_areas(bill.get("average_areas"), weights_rear.get("average_areas"))
        focal_vision_duration_rear = metrics.calculate_focal_vision_duration(bill.get("focal_vision_duration"), weights_rear.get("focal_vision_duration"))
        near_p_duration_rear = metrics.calculate_near_p_duration(bill.get("near_p_duration"), weights_rear.get("near_p_duration"))
        mid_p_duration_rear = metrics.calculate_mid_p_duration(bill.get("mid_p_duration"), weights_rear.get("mid_p_duration"))
        far_p_duration_rear = metrics.calculate_far_p_duration(bill.get("far_p_duration"), weights_rear.get("far_p_duration"))
        average_speed_rear = metrics.calculate_average_speed(bill.get("average_speed"), weights_rear.get("average_speed"))

        front_total = (
            distance_to_center_front + average_areas_front + 
            focal_vision_duration_front + near_p_duration_front + 
            mid_p_duration_front + far_p_duration_front + average_speed_front
        )

        rear_total = (
            distance_to_center_rear + average_areas_rear + 
            focal_vision_duration_rear + near_p_duration_rear + 
            mid_p_duration_rear + far_p_duration_rear + average_speed_rear
        )

        saliency_front = metrics.calculate_saliency(front_total)
        saliency_rear = metrics.calculate_saliency(rear_total)
        saliency_net = metrics.calculate_net_saliency(saliency_front, saliency_rear)

        q = """
            UPDATE billboards 
            SET 
                saliency_score_front_city=%s,
                saliency_score_rear_city=%s,
                net_saliency_score_city=%s
            WHERE
                id=%s
        """

        query_db(q, (saliency_front, saliency_rear, saliency_net, bill_id))

    query_db("COMMIT")

    billoards_q =   '''
        SET @rank = 0;
        CREATE TEMPORARY TABLE temp_ranking AS
        SELECT b.id, (@rank := @rank + 1) AS rank
        FROM billboards b
        JOIN videofiles v ON b.video_id = v.video_id
        WHERE v.city_id = %s
        ORDER BY b.net_saliency_score_city DESC;
'''
    query_db(billoards_q, (city_id,))
    show_temp_table_q = '''
            SHOW TABLES LIKE 'temp_ranking';
        '''
    result = query_db(show_temp_table_q)

    if result:
            # Temporary table exists, fetch and print its contents
        fetch_temp_table_q = '''
                SELECT * FROM temp_ranking;
            '''
        temp_results = query_db(fetch_temp_table_q)

            # Print or process the results
        print("Contents of temp_ranking:")
        for row in temp_results:
                print(row)  # Print each row to console for inspection

    else:
        print("Temporary table temp_ranking does not exist.")

    billoards_q = '''UPDATE billboards b
    JOIN temp_ranking tr ON b.id = tr.id
    SET b.Rank_net_saliency_citywise = tr.rank;
    DROP TEMPORARY TABLE IF EXISTS temp_ranking;'''
    query_db(billoards_q, ())

    
    query_db("COMMIT")



    return jsonify({'message': 'Saliency calculated successfully'}), 201




    

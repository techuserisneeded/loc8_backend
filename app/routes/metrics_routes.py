import os
from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
import re

from app.utils.helpers import token_required, superadmin_required, admin_required
from app.utils.db_helper import query_db
import app.utils.metrics as metrics
from app.utils.helpers import clean_and_lower, generate_bcrypt_hash, generate_uuid

from app.constants.roles import roles
from app.services.users import is_user_email_exits, is_emp_id_exits
from app.services.user_areas import insert_user_areas
from app.constants.default_weights import default_weights_front, default_weights_rear
from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon, Feature


metrics_bp = Blueprint('metrics', __name__)

@metrics_bp.route("/estimateimpression", methods=['POST'])
@token_required
def estimate_impression(current_user):
    try:
        q = '''
        SELECT COALESCE(latitude, 0) AS latitude, COALESCE(longitude, 0) AS longitude, id, impression_id, effective_impression, net_saliency_score_city
        FROM billboards as b
        '''
        billboard = query_db(q)

        query_q = '''SELECT impression_id, impression, lat1, long1, lat2, long2, lat3, long3, lat4, long4, lat5, long5, lat6, long6, lat7, long7 
        FROM impression_data
        '''
        impressions = query_db(query_q)
        for bill in billboard:
            for impression in impressions:
                point = Feature(geometry=Point((bill.get('latitude'), bill.get('longitude'))))
                polygon = Polygon(
                    [
                        [
                            (impression.get('lat1'), impression.get('long1')),
                            (impression.get('lat2'), impression.get('long2')),
                            (impression.get('lat3'), impression.get('long3')),
                            (impression.get('lat4'), impression.get('long4')),
                            (impression.get('lat5'), impression.get('long5')),
                            (impression.get('lat6'), impression.get('long6')),
                            (impression.get('lat7'), impression.get('long7')),
                        ]
                    ]
                )

                if(boolean_point_in_polygon(point, polygon)):
                    
                    effective_impression_val = bill.get('net_saliency_score_city')*impression.get('impression')
                    q = '''UPDATE billboards
                    SET impression_id = %s, effective_impression = %s
                    where id= %s'''
                    query_db(q, (impression.get('impression_id'),effective_impression_val, bill.get('id')))
                    query_db("COMMIT")
                    break
        return jsonify({'message': 'Impression Estimated Successfully'}), 201 
    except Exception as e:
        print(str(e))
        query_db("ROLLBACK")
        return jsonify({'message': 'something went wrong'}), 500




@metrics_bp.route("/impression", methods=['POST'])
@token_required
def add_impression(current_user):
    body = request.get_json()
    data = body.get("data")
    
    try:
        for i in range(0,len(data) - 1):
            row = data[i]['WKT']
            impression = data[i]['Impressions']
            numbers = re.findall(r'\d+\.?\d*', row)
            # Convert the extracted numbers from strings to integers or floats
            numbers = [float(num) for num in numbers]
            if len(numbers) == 14 and impression and type(numbers[0]) == float and type(numbers[1]) == float and type(numbers[2]) == float and type(numbers[3]) == float and type(numbers[4]) == float and type(numbers[5]) == float and type(numbers[6]) == float and type(numbers[7]) == float and type(numbers[8]) == float and type(numbers[9]) == float and type(numbers[10]) == float and type(numbers[11]) == float and type(numbers[12]) == float and type(numbers[13]) == float:            
                long1  = numbers[0],
                
                lat1 = numbers[1],
                
                long2  = numbers[2],
                lat2 = numbers[3],
                long3  = numbers[4],
                lat3 = numbers[5],
                long4  = numbers[6],
                lat4 = numbers[7],
                long5  = numbers[8],
                lat5 = numbers[9],
                long6  = numbers[10],
                lat6 = numbers[11],
                long7  = numbers[12],
                lat7 = numbers[13],
                # print()

                insert_q = """
                INSERT INTO impression_data(lat1,
                        long1,
                        lat2,
                        long2,
                        lat3,
                        long3,
                        lat4,
                        long4,
                        lat5,
                        long5,
                        lat6,
                        long6,
                        lat7,
                        long7, 
                        impression)
                            VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)
                 """
                query_db(insert_q, (lat1[0],long1[0],lat2[0],long2[0],lat3[0],long3[0],lat4[0],long4[0],lat5[0],long5[0],lat6[0],long6[0],lat7[0],long7[0], impression))
        query_db("COMMIT")

        return jsonify({'message': 'Impression Added Successfully'}), 201 
    except Exception as e:
        print(str(e))
        query_db("ROLLBACK")
        return jsonify({'message': 'something went wrong'}), 500



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
    is_city_checked = body.get("iscitychecked")
    is_location_checked = body.get("islocationchecked")
    body_weights_front = body.get("front_weightings", {})
    body_weights_rear = body.get("rear_weightings", {})

    print(is_city_checked, is_location_checked)

    weights_front = {
        "distance_to_center": body_weights_front.get("distance_to_center") or default_weights_front.get("distance_to_center"),
        "average_areas": body_weights_front.get("average_areas") or default_weights_front.get("average_areas"),
        "focal_vision_duration": body_weights_front.get("focal_vision_duration") or default_weights_front.get("focal_vision_duration"),
        "near_p_duration": body_weights_front.get("near_p_duration") or default_weights_front.get("near_p_duration"),
        "mid_p_duration": body_weights_front.get("mid_p_duration") or default_weights_front.get("mid_p_duration"),
        "far_p_duration": body_weights_front.get("far_p_duration") or default_weights_front.get("far_p_duration"),
        "average_speed": body_weights_front.get("average_speed") or default_weights_front.get("average_speed"),
        "saliency": body_weights_front.get("saliency") or default_weights_front.get("saliency"),
    }

    weights_rear = {
        "distance_to_center": body_weights_rear.get("distance_to_center") or default_weights_rear.get("distance_to_center"),
        "average_areas": body_weights_rear.get("average_areas") or default_weights_rear.get("average_areas"),
        "focal_vision_duration": body_weights_rear.get("focal_vision_duration") or default_weights_rear.get("focal_vision_duration"),
        "near_p_duration": body_weights_rear.get("near_p_duration") or default_weights_rear.get("near_p_duration"),
        "mid_p_duration": body_weights_rear.get("mid_p_duration") or default_weights_rear.get("mid_p_duration"),
        "far_p_duration": body_weights_rear.get("far_p_duration") or default_weights_rear.get("far_p_duration"),
        "average_speed": body_weights_rear.get("average_speed") or default_weights_rear.get("average_speed"),
        "saliency": body_weights_rear.get("saliency") or default_weights_rear.get("saliency"),
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

    try:
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
            
            saliency_net = metrics.calculate_net_saliency(
                saliency_front,
                weights_front.get("saliency"), 
                saliency_rear, 
                weights_rear.get("saliency")
            )

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
        

        # Ranking Net Saliency citywise
        billoards_q =   '''
        SELECT b.id,b.net_saliency_score_city,RANK() 
        OVER ( ORDER BY net_saliency_score_city DESC) as rank_net_saliency_citywise 
        FROM billboards b JOIN videofiles v
        where v.city_id = %s
        '''
        billboard = query_db(billoards_q, (city_id,))
        query_db("START TRANSACTION")
        for bill in billboard:
            bill_id = bill.get("id")
            q = """
            UPDATE billboards 
            SET 
                rank_net_saliency_citywise=%s
            WHERE
                id=%s
            """
            query_db(q, (bill.get('rank_net_saliency_citywise'),bill_id))
        query_db("COMMIT")


        # Front saliency Ranking citywise
        billoards_q =   '''
        SELECT b.id,b.saliency_score_front_city,RANK() 
        OVER ( ORDER BY saliency_score_front_city DESC) as rank_front_saliency_citywise 
        FROM billboards b JOIN videofiles v
        where v.city_id = %s
        '''

        billboard = query_db(billoards_q, (city_id,))
        
        query_db("START TRANSACTION")
        for bill in billboard:
            bill_id = bill.get("id")
            q = """
            UPDATE billboards 
            SET 
                rank_front_saliency_citywise=%s
            WHERE
                id=%s
            """
            query_db(q, (bill.get('rank_front_saliency_citywise'),bill_id))
        query_db("COMMIT")


        # rear saliency ranking citywise
        billoards_q =   '''
        SELECT b.id,b.saliency_score_rear_city,RANK() 
        OVER ( ORDER BY saliency_score_rear_city DESC) as rank_rear_saliency_citywise 
        FROM billboards b JOIN videofiles v
        where v.city_id = %s
        '''
        billboard = query_db(billoards_q, (city_id,))
        
        query_db("START TRANSACTION")
        for bill in billboard:
            bill_id = bill.get("id")
            q = """
            UPDATE billboards 
            SET 
                rank_rear_saliency_citywise=%s
            WHERE
                id=%s
            """
            query_db(q, (bill.get('rank_rear_saliency_citywise'),bill_id))
        query_db("COMMIT")

    except Exception as e:
        print(str(e))
        query_db("ROLLBACK")
        return jsonify({'message': 'something went wrong'}), 500


    try:
        if is_location_checked == True:
            billoards_q = """
                        SELECT DISTINCT b.location
            FROM billboards AS b
            INNER JOIN videofiles AS v ON v.video_id = b.video_id
            WHERE v.city_id = %s;
            """
            billboards = query_db(billoards_q, (city_id,))

            for bill in billboards: 
                unique_location = bill.get('location')

                if unique_location != None:

                    ##Rank rear saliency locationwise
                    billoards_q = """
                            Select
                            b.id, b.video_id,b.location, b.saliency_score_rear_city, RANK()
                            OVER ( ORDER BY saliency_score_rear_city DESC) as rank_saliency_rear_locationwise 
                            FROM billboards as b INNER JOIN videofiles as v on v.video_id=b.video_id
                            WHERE
                            v.city_id=%s and b.location=%s 
                            """
                    resultant = query_db(billoards_q, (city_id,unique_location))

                    for res in resultant:
                        res_id = res.get("id")
                        q = """
                        UPDATE billboards 
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
                            b.id, b.video_id,b.location, b.saliency_score_front_city, RANK()
                            OVER ( ORDER BY saliency_score_front_city DESC) as rank_saliency_front_locationwise 
                            FROM billboards as b INNER JOIN videofiles as v on v.video_id=b.video_id
                            WHERE
                            v.city_id=%s and b.location=%s 
                            """
                    resultant = query_db(billoards_q, (city_id,unique_location))

                    for res in resultant:
                        res_id = res.get("id")
                        q = """
                        UPDATE billboards 
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
                                b.id, b.video_id,b.location, b.net_saliency_score_city, RANK()
                                OVER ( ORDER BY net_saliency_score_city DESC) as rank_net_saliency_locationwise 
                                FROM billboards as b INNER JOIN videofiles as v on v.video_id=b.video_id
                                WHERE
                                v.city_id=%s and b.location=%s 
                                """
                    resultant = query_db(billoards_q, (city_id,unique_location))

                    for res in resultant:
                        res_id = res.get("id")
                        q = """
                        UPDATE billboards 
                        SET 
                            rank_net_saliency_locationwise=%s
                        WHERE
                            id=%s
                        """
                        query_db(q, (res.get('rank_net_saliency_locationwise'),res_id))
                query_db("COMMIT")

    except Exception as e:
        print(str(e))
        query_db("ROLLBACK")
        return jsonify({'message': 'something went wrong'}), 500 

    return jsonify({'message': 'Saliency calculated successfully'}), 201 

    


import os
from flask import Blueprint, request, jsonify, abort, send_file, redirect, current_app
from flask_socketio import leave_room, join_room
from app.utils.helpers import token_required
from config.config import AppConfig
from werkzeug.utils import secure_filename
from scripts.video_processing_script import video_processing
from app.utils.db_helper import query_db
from app.utils.helpers import generate_uuid, is_prod, generate_defined_length_uuid
from app.constants.roles import roles
from app import socketio

from app.utils.video_helpers import get_coordinates_from_video, compress_video, calculate_avg_speed_stretched
from app.libs.boto3 import upload_video_to_s3, get_presigned_url, delete_obj


video_bp = Blueprint('videos', __name__)

TARGET_VIDEO_PATH = f"./instance/"

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    socketio.emit('message', {'msg': f'Joined room: {room}'}, room=room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    socketio.send(f'has left the room.', room=room)

@video_bp.route('/uploads/<filename>')
def stream_video(filename):
 
    video_q = 'SELECT * FROM videofiles WHERE filename=%s'
    video_details = query_db(video_q, (filename,))

    if not video_details:
        return abort(401)
    
    if not is_prod():
        video_path = video_details[0]['video_path']

        if not os.path.isfile(video_path):
            return abort(401)
        
        return send_file(video_path, mimetype='video/mp4', as_attachment=False)
    
    file_url = get_presigned_url(video_details[0]['filename'])

    if file_url:
        return redirect(file_url)
    else:
        return abort(500)


@video_bp.route('/', methods=['GET',])
@token_required
def get_all_videos(current_user):

    user_role_id = current_user['role_id']
    user_id = current_user['id']
    video_q = ""
    video_details = []
    response = []

    # if user_role_id == roles.get('SUPERADMIN'):
    #     video_q = """
    #         SELECT 	videofiles.*, states.state_name, cities.city_name, zones.zone_name
    #         FROM videofiles
    #         INNER JOIN states ON videofiles.state_id = states.state_id
    #         INNER JOIN cities ON videofiles.city_id = cities.city_id
    #         INNER JOIN zones ON videofiles.zone_id = zones.zone_id
    #      """

    #     video_details = query_db(video_q, ())

    # else: 
    #     video_q = """
    #      SELECT videofiles.*, states.state_name, cities.city_name, zones.zone_name
    #         FROM videofiles
    #         INNER JOIN states ON videofiles.state_id = states.state_id
    #         INNER JOIN cities ON videofiles.city_id = cities.city_id
    #         INNER JOIN zones ON videofiles.zone_id = zones.zone_id
    #         WHERE videofiles.created_by_user_id = %s
    #     """
    #     video_details = query_db(video_q, (user_id,))

    if user_role_id == roles.get('SUPERADMIN'):
        video_q = """
            SELECT 	billboards.*, 
                    videofiles.filename, videofiles.video_path, 
                    videofiles.created_at, videofiles.created_by_user_id,
                    states.state_name, cities.city_name, zones.zone_name
            FROM billboards
            INNER JOIN videofiles ON billboards.video_id = videofiles.video_id
            INNER JOIN states ON videofiles.state_id = states.state_id
            INNER JOIN cities ON videofiles.city_id = cities.city_id
            INNER JOIN zones ON videofiles.zone_id = zones.zone_id
         """

        video_details = query_db(video_q, ())

    else: 
        video_q = """
        SELECT 	billboards.*, 
                    videofiles.filename, videofiles.video_path, 
                    videofiles.created_at, videofiles.created_by_user_id,
                    states.state_name, cities.city_name, zones.zone_name
            FROM billboards
            JOIN videofiles ON billboards.video_id = videofiles.video_id
            JOIN states ON videofiles.state_id = states.state_id
            JOIN cities ON videofiles.city_id = cities.city_id
            JOIN zones ON videofiles.zone_id = zones.zone_id
            WHERE videofiles.created_by_user_id = %s
        """
        video_details = query_db(video_q, (user_id,))

    coordinates_by_video = {};

    if not video_details:
        video_details = []

    for billboard_details in video_details:

        video_id = billboard_details['video_id']

        if video_id not in coordinates_by_video:
            video_coordinates = query_db("""
                        SELECT * FROM video_coordinates WHERE video_id=%s
                """, (billboard_details['video_id'],))
            coordinates_by_video[video_id] = video_coordinates

        if coordinates_by_video[video_id]:
            for idx, coords in enumerate(coordinates_by_video[video_id]):
                billboard_details['latitude' + str(idx)] = coords['latitude']
                billboard_details['longitude'+ str(idx)] = coords['longitude']
                billboard_details['speed'+ str(idx)] = coords['speed']

        else:
            for idx in range(7):
                billboard_details['latitude' + str(idx)] = 0
                billboard_details['longitude'+ str(idx)] = 0
                billboard_details['speed'+ str(idx)] = 0

            response.append(billboard_details)

    
    return jsonify(video_details), 200


@video_bp.route('/upload', methods=['POST',])
@token_required
def upload(current_user):
    video_file = request.files['video']
    zone_id = request.form['zone_id']
    state_id = request.form['state_id']
    city_id = request.form['city_id']
    room_id = request.form['room_id']

    if video_file is None or video_file.filename == "":
        return jsonify({"error": "no file"})

    unique_id = generate_defined_length_uuid(6) 

    original_filename = secure_filename(video_file.filename)
    filename_wo_ext, file_extension = os.path.splitext(original_filename)

    raw_filename = secure_filename(generate_uuid() + video_file.filename)
    filename = secure_filename(f"{filename_wo_ext}_{unique_id}{file_extension}")
    processed_filename = secure_filename("temp_" + filename)

    raw_file_path = os.path.abspath(os.path.join(AppConfig.UPLOAD_FOLDER, raw_filename))
    processed_file_path = os.path.abspath(os.path.join(TARGET_VIDEO_PATH, processed_filename))
    compressed_file_path = os.path.abspath(os.path.join(TARGET_VIDEO_PATH, filename))

    video_file.save(raw_file_path)

    def progress_callback(progress_percentage, message="OOH Asset Detection & Feature Extraction in progress"):
        socketio.emit('processing_progress', {'percentage': progress_percentage, 'message': message}, room=room_id)

    def progress_callback_s3(progress_percentage):
        socketio.emit('processing_progress', {'percentage': progress_percentage, 'message': 'saving...'}, room=room_id)

    vcd = video_processing(raw_file_path, processed_file_path, progress_callback)
    vcd2 = str(vcd)
    vcd3 = vcd2[0:2]

    progress_callback(-1, "compressing...")

    compress_video(processed_file_path, compressed_file_path)

    progress_callback(100, "compressing...")

    s3_file_url = compressed_file_path

    if is_prod():
        s3_file_url = upload_video_to_s3(compressed_file_path, filename, progress_callback=progress_callback_s3)

    video_id = insert_video_data(s3_file_url, filename, zone_id, state_id, city_id, current_user['id'])
    insert_billboard_data(video_id, current_user['id'], vcd)

    # video_id = insert_video_data(compressed_file_path, comp_filename, zone_id, state_id, city_id, current_user['id'])
    # insert_billboard_data(video_id, current_user['id'], vcd)

    coordinate_tuples = get_coordinates_from_video(raw_file_path)

    coordinates_q = """
        INSERT INTO `video_coordinates`(`video_id`, `speed`, `latitude`, `longitude`) 
        VALUES (%s, %s, %s, %s)
    """
    for coords in coordinate_tuples:
        query_db(coordinates_q, (video_id, coords[0], coords[1], coords[2]), False, True)

    bill_q = "SELECT * FROM billboards WHERE video_id = %s";
    billboards = query_db(bill_q, (video_id,))
   
    video_q = "SELECT * FROM videofiles WHERE video_id = %s";
    video_details = query_db(video_q, (video_id,), True)

    os.remove(raw_file_path)
    os.remove(processed_file_path)

    if is_prod():
        os.remove(compressed_file_path)

    return jsonify({"billboards":  billboards, "video_details": video_details}), 200
    # return jsonify({"billboards":  "", "video_details": ""}), 200


@video_bp.route('/output/<video_id>', methods=['GET',])
@token_required
def processed_output(current_user,video_id):

    video_q = """
        SELECT  v.video_id, 
                v.filename,
                v.video_path, 
                z.zone_name, 
                s.state_name, 
                c.city_name, 
                v.created_at, 
                v.created_by_user_id
        FROM videofiles v
        JOIN zones z ON v.zone_id = z.zone_id
        JOIN states s ON v.state_id = s.state_id
        JOIN cities c ON v.city_id = c.city_id
        WHERE v.video_id = %s;
    """
    video_details = query_db(video_q, (video_id,), True)

    bill_q = "SELECT * FROM billboards WHERE video_id = %s ORDER BY tracker_id ASC";
    billboards = query_db(bill_q, (video_id,))

    video_q = """
        SELECT * FROM video_coordinates
        WHERE video_id=%s
    """

    video_coordinates = query_db(video_q, (video_id,))

    if not video_coordinates:
        video_coordinates = []

    avg_speed_km, stretched_in_meters = calculate_avg_speed_stretched(video_coordinates)

    return jsonify({
        "billboards":  billboards, 
        "video_details": video_details, 
        'video_coordinates': video_coordinates, 
        'avg_speed_km': avg_speed_km, 
        'stretched_in_meters': stretched_in_meters
    }), 200

@video_bp.route('/videos/<video_id>', methods=['DELETE'])
@token_required
def delete_video(current_user, video_id):

    user_id = current_user['id']
    user_role_id = current_user['role_id']
    
    video_q = 'SELECT * FROM videofiles WHERE video_id=%s'
    video_details = query_db(video_q, (video_id,), one=True)

    if not video_details:
        return abort(404)

    if user_role_id == roles.get('SUPERADMIN') or video_details['created_by_user_id'] == user_id:

        try:
            query_db("START TRANSACTION")

            q = "DELETE FROM video_coordinates WHERE video_id=%s"
            query_db(q, (video_id,))

            q = "DELETE FROM billboards WHERE video_id=%s"
            query_db(q, (video_id,))

            q = "DELETE FROM videofiles WHERE video_id=%s"
            query_db(q, (video_id,))

            if not is_prod():
                os.remove(video_details['video_path'])
            else:
                delete_obj(object_name=video_details['filename'])

            query_db("COMMIT")

            return jsonify({"message": "Deleted successfully!"})
        except:
            query_db("ROLLBACK")
            return jsonify({"message": "Unable to delete!"}),500
    else:
        return jsonify({"message": "You are unauthorized!"}), 401


@video_bp.route('/billboards/merge', methods=['POST'])
@token_required
def merge_billborads(current_user):
    data = request.get_json()
    billboard_ids = data.get('billboard_ids', [])

    if not billboard_ids:
        return jsonify({"error": "No billboard IDs provided"}), 400
    
    new_billboard_id = generate_uuid()

    query_merge_sum_average = f"""
        INSERT INTO billboards (id, video_id, visibility_duration, distance_to_center, central_duration, near_p_duration, 
                                mid_p_duration, far_p_duration, central_distance, near_p_distance, mid_p_distance, 
                                far_p_distance, average_areas, confidence, tracker_id, created_by_user_id)
        SELECT
            %s,
            video_id,
            SUM(visibility_duration) AS visibility_duration_sum,
            SUM(distance_to_center) AS distance_to_center_sum,
            SUM(central_duration) AS central_duration_sum,
            SUM(near_p_duration) AS near_p_duration_sum,
            SUM(mid_p_duration) AS mid_p_duration_sum,
            SUM(far_p_duration) AS far_p_duration_sum,
            SUM(central_distance) AS central_distance_sum,
            SUM(near_p_distance) AS near_p_distance_sum,
            SUM(mid_p_distance) AS mid_p_distance_sum,
            SUM(far_p_distance) AS far_p_distance_sum,
            AVG(average_areas) AS average_areas_avg,
            AVG(confidence) AS confidence_avg,
            MAX(tracker_id) AS tracker_id,
            created_by_user_id
        FROM billboards
        WHERE id IN ({','.join(['%s']*len(billboard_ids))})
        GROUP BY video_id, created_by_user_id
    """

    query_db(query_merge_sum_average, (new_billboard_id, *billboard_ids), False, True)

    query_delete_previous_rows = f"""
        DELETE FROM billboards
        WHERE id IN ({','.join(['%s']*len(billboard_ids))})
    """
    query_db(query_delete_previous_rows, tuple(billboard_ids), False, True)

    return jsonify({"message": "Merge successful"}), 200


@video_bp.route('/billboards/delete', methods=['POST'])
@token_required
def delete_billboards(current_user):
    data = request.get_json()
    billboard_ids = data.get('billboard_ids', [])

    if not billboard_ids:
        return jsonify({'message': 'No billboard IDs provided'}), 400

    q = """
        DELETE FROM billboards WHERE id IN ({})
    """.format(','.join('%s' for _ in billboard_ids))

    query_db(q, billboard_ids, commit=True)

    return jsonify({ "message": "saved successfully!"})

def insert_video_data(output_file_path, filename, zone_id, state_id, city_id, created_by_user_id):
    video_query = """
        INSERT INTO videofiles (video_id, filename, video_path, zone_id, state_id, city_id, created_by_user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    video_id = generate_uuid()
    video_args = (video_id, filename, output_file_path, zone_id, state_id, city_id, created_by_user_id)
    query_db(video_query, video_args, False, True)
    return video_id

def insert_billboard_data(video_id, user_id, billboard_data):
    for tracker_id, data in billboard_data.items():
        bill_id = generate_uuid()
        visibility_duration = round(data.get('visibility_duration', 0), 2)
        distance_to_center = round(data.get('distance_to_center', 0), 2)
        central_duration = round(data['BillBoard_Region_Duration and Distance'].get('Central', 0), 2)
        near_p_duration = round(data['BillBoard_Region_Duration and Distance'].get('Near P', 0), 2)
        mid_p_duration = round(data['BillBoard_Region_Duration and Distance'].get('Mid P', 0), 2)
        far_p_duration = round(data['BillBoard_Region_Duration and Distance'].get('Far P', 0), 2)
        central_distance = round(data['BillBoard_Region_Duration and Distance'].get('Central Dist', 0), 2)
        near_p_distance = round(data['BillBoard_Region_Duration and Distance'].get('Near P Dist', 0), 2)
        mid_p_distance = round(data['BillBoard_Region_Duration and Distance'].get('Mid P Dist', 0), 2)
        far_p_distance = round(data['BillBoard_Region_Duration and Distance'].get('Far P Dist', 0), 2)
        average_areas = round(data.get('Average Areas', 0), 2)
        confidence = round(data.get('Confidence', 0), 2)

        billboard_query = """
            INSERT INTO billboards (id, video_id, visibility_duration, distance_to_center, central_duration, near_p_duration, mid_p_duration, far_p_duration, 
                                    central_distance, near_p_distance, mid_p_distance, far_p_distance, average_areas, confidence, tracker_id, created_by_user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        billboard_args = (
            bill_id,
            video_id,
            visibility_duration,
            distance_to_center,
            central_duration,
            near_p_duration,
            mid_p_duration,
            far_p_duration,
            central_distance,
            near_p_distance,
            mid_p_distance,
            far_p_distance,
            average_areas,
            confidence,
            tracker_id,
            user_id
        )
        query_db(billboard_query, billboard_args, False, True)

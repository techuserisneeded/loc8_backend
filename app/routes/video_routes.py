import os
from flask import Blueprint, request, jsonify, send_from_directory,abort, send_file, redirect
from app.utils.helpers import token_required
from config.config import AppConfig
from werkzeug.utils import secure_filename
from scripts.video_processing_script import video_processing
from app.utils.db_helper import query_db
from app.utils.helpers import generate_uuid
from app.constants.roles import roles
from app import socketio

from app.utils.video_helpers import get_coordinates_from_video, compress_video
from app.libs.boto3 import upload_video_to_s3, get_presigned_url


video_bp = Blueprint('videos', __name__)

TARGET_VIDEO_PATH = f"./instance/"

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@video_bp.route('/uploads/<filename>')
def stream_video(filename):

    video_q = 'SELECT * FROM videofiles WHERE filename=%s'
    video_details = query_db(video_q, (filename,))

    if not video_details:
        return abort(401)
    
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
            for idx in range(6):
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

    if video_file is None or video_file.filename == "":
        return jsonify({"error": "no file"})

    dest = os.path.abspath(os.path.join(AppConfig.UPLOAD_FOLDER, secure_filename(video_file.filename)))
    unique_id = generate_uuid()
    filename = secure_filename("temp_" + unique_id + ".mp4")
    output_file_path = os.path.abspath(os.path.join(TARGET_VIDEO_PATH, filename))

    comp_filename = secure_filename(unique_id + ".mp4")
    compressed_file_path = os.path.abspath(os.path.join(TARGET_VIDEO_PATH, comp_filename))

    video_file.save(dest)

    def progress_callback(progress_percentage):
        socketio.emit('processing_progress', {'percentage': progress_percentage}, room=current_user['id'])

    def progress_callback_s3(progress_percentage):
        socketio.emit('saving_processed_video', {'percentage': progress_percentage}, room=current_user['id'])

    vcd = video_processing(dest, output_file_path, progress_callback)
    vcd2 = str(vcd)
    vcd3 = vcd2[0:2]

    socketio.emit('compress_progress', {'percentage': -1}, room=current_user['id'])

    compress_video(output_file_path, compressed_file_path)

    socketio.emit('compress_progress', {'percentage': 100}, room=current_user['id'])

    s3_file_url = upload_video_to_s3(compressed_file_path, comp_filename, progress_callback=progress_callback_s3)

    video_id = insert_video_data(s3_file_url, comp_filename, zone_id, state_id, city_id, current_user['id'])
    insert_billboard_data(video_id, current_user['id'], vcd)

    # video_id = insert_video_data(compressed_file_path, comp_filename, zone_id, state_id, city_id, current_user['id'])
    # insert_billboard_data(video_id, current_user['id'], vcd)

    coordinate_tuples = get_coordinates_from_video(dest)

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

    os.remove(dest)
    os.remove(output_file_path)
    os.remove(compressed_file_path)

    return jsonify({"billboards":  billboards, "video_details": video_details}), 200
    # return jsonify({"billboards":  "", "video_details": ""}), 200


@video_bp.route('/output/<video_id>', methods=['GET',])
@token_required
def processed_output(current_user,video_id):
    bill_q = "SELECT * FROM billboards WHERE video_id = %s ORDER BY tracker_id ASC";
    billboards = query_db(bill_q, (video_id,))
   
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

    video_q = """
        SELECT * FROM video_coordinates
        WHERE video_id=%s
    """

    video_coordinates = query_db(video_q, (video_id,))

    if not video_coordinates:
        video_coordinates = []

    return jsonify({"billboards":  billboards, "video_details": video_details, 'video_coordinates': video_coordinates}), 200

@video_bp.route('/billboards/merge', methods=['POST'])
@token_required
def merge_billborads(current_user):
    data = request.get_json()
    billboard_ids = data.get('billboard_ids', [])
    user_id = current_user['id']

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
        GROUP BY video_id
    """

    query_db(query_merge_sum_average, (new_billboard_id, *billboard_ids), False, True)

    query_delete_previous_rows = f"""
        DELETE FROM billboards
        WHERE id IN ({','.join(['%s']*len(billboard_ids))})
    """
    query_db(query_delete_previous_rows, tuple(billboard_ids), False, True)

    return jsonify({"message": "Merge successful"}), 200

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

        bill_id = generate_uuid();
        billboard_query = """
            INSERT INTO billboards (id, video_id, visibility_duration, distance_to_center, central_duration, near_p_duration, mid_p_duration, far_p_duration, 
                                    central_distance, near_p_distance, mid_p_distance, far_p_distance, average_areas, confidence, tracker_id, created_by_user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        billboard_args = (
            bill_id,
            video_id,
            data['visibility_duration'],
            data['distance_to_center'],
            data['BillBoard_Region_Duration and Distance']['Central'],
            data['BillBoard_Region_Duration and Distance']['Near P'],
            data['BillBoard_Region_Duration and Distance']['Mid P'],
            data['BillBoard_Region_Duration and Distance']['Far P'],
            data['BillBoard_Region_Duration and Distance']['Central Dist'],
            data['BillBoard_Region_Duration and Distance']['Near P Dist'],
            data['BillBoard_Region_Duration and Distance']['Mid P Dist'],
            data['BillBoard_Region_Duration and Distance']['Far P Dist'],
            data['Average Areas'],
            data['Confidence'],
            tracker_id,
            user_id
        )
        query_db(billboard_query, billboard_args, False, True)
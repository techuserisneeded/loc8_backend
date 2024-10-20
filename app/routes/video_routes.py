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
from app.constants.global_variables import ABORT_REQUESTS_ROOMS

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
                    videofiles.created_at, videofiles.created_by_user_id, videofiles.length_of_stretch, videofiles.average_speed,
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
                    videofiles.created_at, videofiles.created_by_user_id, videofiles.length_of_stretch, videofiles.average_speed,
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

    # for billboard_details in video_details:

    #     video_id = billboard_details['video_id']

    #     if video_id not in coordinates_by_video:
    #         video_coordinates = query_db("""
    #                     SELECT * FROM video_coordinates WHERE video_id=%s
    #             """, (billboard_details['video_id'],))
    #         coordinates_by_video[video_id] = video_coordinates

    #     if coordinates_by_video[video_id]:
    #         for idx, coords in enumerate(coordinates_by_video[video_id]):
    #             billboard_details['latitude' + str(idx)] = coords['latitude']
    #             billboard_details['longitude'+ str(idx)] = coords['longitude']
    #             billboard_details['speed'+ str(idx)] = coords['speed']

    #     else:
    #         for idx in range(7):
    #             billboard_details['latitude' + str(idx)] = 0
    #             billboard_details['longitude'+ str(idx)] = 0
    #             billboard_details['speed'+ str(idx)] = 0

    #         response.append(billboard_details)

    
    return jsonify(video_details), 200


@video_bp.route('/upload', methods=['POST',])
@token_required
def upload(current_user):
    video_file = request.files['video']
    zone_id = request.form['zone_id']
    state_id = request.form['state_id']
    city_id = request.form['city_id']
    room_id = request.form['room_id']
    overwrite = request.form['overwrite']
        
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

    video_name_like = filename_wo_ext + "_%"
    
    video_id = None
    is_video_present = False

    query = '''SELECT *
        FROM videofiles
        WHERE filename LIKE %s
        AND city_id=%s
    '''
    videos_in_city = query_db(query, (video_name_like, city_id))

    if len(videos_in_city) > 0:
        video_id = videos_in_city[0]["video_id"]
        is_video_present = True
        
    if not overwrite and is_video_present:
       return jsonify({ 'message': 'filename for the city already exists.' }), 409

    chunk_size = 1024 * 1024

    f = open(raw_file_path, 'wb')

    while True:
        if room_id in ABORT_REQUESTS_ROOMS:
            f.close()
            os.remove(raw_file_path)
            ABORT_REQUESTS_ROOMS.remove(room_id)
            return jsonify({"message": "Upload aborted during file save"}), 400
        
        chunk = video_file.stream.read(chunk_size)
        
        if not chunk:
            break
    
        f.write(chunk)

    f.close()
        
    def progress_callback(progress_percentage, message="OOH Asset Detection & Feature Extraction in progress"):

        if room_id in ABORT_REQUESTS_ROOMS:
            os.remove(raw_file_path)
            os.remove(processed_file_path)
            socketio.emit('processing_aborted', {'message': 'Video processing aborted'}, room=room_id)
            ABORT_REQUESTS_ROOMS.remove(room_id)
            return jsonify({"message": "Processing aborted"}), 400
        
        socketio.emit('processing_progress', {'percentage': progress_percentage, 'message': message}, room=room_id)

    def progress_callback_s3(progress_percentage):
        if room_id in ABORT_REQUESTS_ROOMS:
            try:
                os.remove(compressed_file_path)
            except:
                pass

            socketio.emit('processing_aborted', {'message': 'Video processing aborted'}, room=room_id)
            ABORT_REQUESTS_ROOMS.remove(room_id)
            raise Exception("Upload aborted by user")
        
        socketio.emit('processing_progress', {'percentage': progress_percentage, 'message': 'saving...'}, room=room_id)

    vcd = video_processing(raw_file_path, processed_file_path, progress_callback, room_id=room_id)

    if room_id in ABORT_REQUESTS_ROOMS:
        os.remove(raw_file_path)  

        if os.path.exists(processed_file_path):
            os.remove(processed_file_path)

        ABORT_REQUESTS_ROOMS.remove(room_id)
        return jsonify({"message": "Processing aborted"}), 400

    progress_callback(-1, "compressing...")

    compress_video(processed_file_path, compressed_file_path, room_id)

    if room_id in ABORT_REQUESTS_ROOMS:
        os.remove(raw_file_path)  

        if os.path.exists(processed_file_path):
            os.remove(processed_file_path)

        if os.path.exists(compressed_file_path):
            os.remove(compressed_file_path)

        ABORT_REQUESTS_ROOMS.remove(room_id)
        return jsonify({"message": "Processing aborted"}), 400

    progress_callback(100, "compressing...")

    s3_file_url = compressed_file_path

    if is_prod():
        try:
            s3_file_url = upload_video_to_s3(compressed_file_path, filename, progress_callback=progress_callback_s3)
        except Exception as e:
            if "aborted by user" in str(e).lower():
                return jsonify({"message": "Video processing was aborted."}), 400
            else:
                return jsonify({"message": "Something went wrong while uploading the video."}), 500
            
    query_db("START TRANSACTION")

    if is_video_present:

        #delete co-ordinates
        q = """
            DELETE FROM video_coordinates WHERE video_id=%s
        """
        v = (video_id,)

        query_db(q, v)

        #delete billboards data
        q = """
            DELETE FROM billboards WHERE video_id=%s
        """
        v = (video_id,)

        query_db(q, v)

        #delete video data
        q = """
            DELETE FROM videofiles WHERE video_id=%s
        """
        v = (video_id,)

        query_db(q, v)


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
        query_db(coordinates_q, (video_id, coords[0], coords[1], coords[2]))

    coordinates_q = """
        SELECT * FROM video_coordinates
        WHERE video_id=%s
    """

    video_coordinates = query_db(coordinates_q, (video_id,))

    if not video_coordinates:
        video_coordinates = []

    avg_speed_km, stretched_in_meters = calculate_avg_speed_stretched(video_coordinates)

    query = """
        UPDATE videofiles
        SET
            average_speed=%s, 
            length_of_stretch=%s
        WHERE
            video_id=%s
    """

    args = (
        avg_speed_km,
        stretched_in_meters,
        video_id
    )

    query_db(query, args)

    query_db("COMMIT")

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


@video_bp.route('/upload/abort', methods=['POST'])
@token_required
def abort_video(current_user):
    room_id = request.form['room_id']

    ABORT_REQUESTS_ROOMS.append(room_id)

    socketio.emit('processing_aborted', {'message': 'Video processing aborted'}, room=room_id)
    
    return jsonify({"message": "Video upload aborted"}), 200



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

            if not is_prod() and os.path.exists(video_details['video_path']):
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
    selected_id = data.get('selected_id', "")

    if not billboard_ids:
        return jsonify({"error": "No billboard IDs provided"}), 400
    
    if not selected_id:
        return jsonify({"error": "No selected id was provided"}), 400
    
    if selected_id not in billboard_ids:
        return jsonify({"error": "Selected ID must be one of the billboard IDs"}), 400

    query_create_temp_table = f"""
        CREATE TEMPORARY TABLE temp_billboard_aggregate AS
        SELECT
            SUM(visibility_duration) AS visibility_duration_sum,
            AVG(distance_to_center) AS distance_to_center_avg,
            SUM(central_duration) AS central_duration_sum,
            SUM(near_p_duration) AS near_p_duration_sum,
            SUM(mid_p_duration) AS mid_p_duration_sum,
            SUM(far_p_duration) AS far_p_duration_sum,
            AVG(central_distance) AS central_distance_avg,
            AVG(near_p_distance) AS near_p_distance_avg,
            AVG(mid_p_distance) AS mid_p_distance_avg,
            AVG(far_p_distance) AS far_p_distance_avg,
            AVG(average_areas) AS average_areas_avg,
            AVG(confidence) AS confidence_avg,
            MAX(tracker_id) AS tracker_id
        FROM billboards
        WHERE id IN ({','.join(['%s']*len(billboard_ids))})
    """
    query_db(query_create_temp_table, tuple(billboard_ids), False, True)

    query_update_selected = """
        UPDATE billboards
        JOIN temp_billboard_aggregate ON TRUE
        SET
            billboards.visibility_duration = temp_billboard_aggregate.visibility_duration_sum,
            billboards.distance_to_center = temp_billboard_aggregate.distance_to_center_avg,
            billboards.central_duration = temp_billboard_aggregate.central_duration_sum,
            billboards.near_p_duration = temp_billboard_aggregate.near_p_duration_sum,
            billboards.mid_p_duration = temp_billboard_aggregate.mid_p_duration_sum,
            billboards.far_p_duration = temp_billboard_aggregate.far_p_duration_sum,
            billboards.central_distance = temp_billboard_aggregate.central_distance_avg,
            billboards.near_p_distance = temp_billboard_aggregate.near_p_distance_avg,
            billboards.mid_p_distance = temp_billboard_aggregate.mid_p_distance_avg,
            billboards.far_p_distance = temp_billboard_aggregate.far_p_distance_avg,
            billboards.average_areas = temp_billboard_aggregate.average_areas_avg,
            billboards.confidence = temp_billboard_aggregate.confidence_avg,
            billboards.tracker_id = temp_billboard_aggregate.tracker_id
        WHERE billboards.id = %s
    """
    query_db(query_update_selected, (selected_id,), False, True)

    query_delete_previous_rows = f"""
        DELETE FROM billboards
        WHERE id IN ({','.join(['%s']*len(billboard_ids))}) AND id != %s
    """
    query_db(query_delete_previous_rows, (*billboard_ids, selected_id), False, True)

    return jsonify({"message": "Merge successful"}), 200

@video_bp.route('/billboards/asset-info/<billboard_id>', methods=['PUT'])
@token_required
def add_asset_info(current_user, billboard_id):

    current_user_id = current_user['id']

    data = request.form

    #data
    media_type = data['media_type']
    illumination = data['illumination']
    vendor_name = data['vendor_name']
    traffic_direction = data['traffic_direction']

    location = data['location']
    latitude = float(data['latitude'])
    longitude = float(data['longitude'])

    duration = float(data['duration'])
    mounting_rate = float(data['mounting_rate'])
    printing_rate = float(data['printing_rate'])
    rental_per_month = float(data['rental_per_month'])

    height = float(data['height'])
    width = float(data['width'])
    qty = int(data['quantity'])

    cost_for_duration = (rental_per_month * duration) / 30

    asset_data = query_db("SELECT * FROM billboards WHERE id=%s", (billboard_id,), one=True)

    map_img_filename = asset_data.get("map_image") or None
    site_img_filename = asset_data.get("site_image") or None

    map_image_file = None
    site_image_file = None

    if 'map_image' in request.files:
        map_image_file = request.files['map_image']
        if map_image_file.filename != '':
            map_img_filename = generate_uuid() + secure_filename(map_image_file.filename)

    if 'site_image' in request.files:
        site_image_file = request.files['site_image']
        if site_image_file.filename != '':
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
            duration=%s, 
            rental_per_month=%s, 
            printing_rate=%s,
            mounting_rate=%s, 
            cost_for_duration=%s, 
            map_image=%s, 
            site_image=%s,
            vendor_name=%s,
            traffic_direction=%s
        WHERE
            id=%s
    """

    args = (
        location, latitude, longitude,
        illumination, media_type, width,
        height, qty, 
        duration, rental_per_month, 
        printing_rate, mounting_rate, cost_for_duration,
        map_img_filename, site_img_filename, vendor_name,
        traffic_direction, billboard_id
    )

    query_db(query, args, True, True)

    if map_image_file:
        map_image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], map_img_filename))
    
    if site_image_file:
        site_image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], site_img_filename))

    return jsonify({'message': 'Plan added successfully'}), 201


@video_bp.route('/billboards/asset-info/<billboard_id>', methods=['GET'])
@token_required
def get_asset_info(current_user, billboard_id):
    q = """
        SELECT * FROM billboards WHERE id=%s
    """

    billboard = query_db(q, (billboard_id,), True)

    if billboard == None:
        return jsonify(""), 200
    
    q = """
        SELECT * FROM video_coordinates WHERE video_id=%s
    """
    
    video_coordinates = query_db(q, (billboard['video_id'],))

    q = """
        SELECT * FROM videofiles WHERE video_id=%s
    """
    
    video = query_db(q, (billboard['video_id'],), True)

    return jsonify({"asset" : billboard, "video_coordinates" : video_coordinates, "video": video}), 200
    
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
    query_db(video_query, video_args) # make sure to commit, here we are not committing
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
        query_db(billboard_query, billboard_args) # make sure to commit, here we are not committing



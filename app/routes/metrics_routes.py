import os
from flask import Blueprint, jsonify, request, current_app
from app.utils.helpers import token_required, superadmin_required, admin_required
from app.utils.db_helper import query_db
from werkzeug.utils import secure_filename
from app.utils.helpers import clean_and_lower, generate_bcrypt_hash, generate_uuid
from app.constants.roles import roles
from app.services.users import is_user_email_exits, is_emp_id_exits
from app.services.user_areas import insert_user_areas

metrics_bp = Blueprint('metrics', __name__)

@metrics_bp.route('/saliency', methods=['POST'])
@token_required
def calculate_saliency(current_user):

    current_user_id = current_user['id']

    body = request.get_json()

    zone_id = body.get("zone_id")
    state_id = body.get("state_id")
    city_id = body.get("city_id")
    level = body.get("level", "city")

    

    return jsonify({'message': 'Saliency calculated successfully'}), 201
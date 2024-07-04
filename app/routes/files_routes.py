from flask import Blueprint, request, jsonify, send_from_directory, abort
from app.utils.helpers import token_required, superadmin_required
from app.utils.db_helper import query_db

files_bp = Blueprint('files', __name__)

@files_bp.route('/images/<path:filename>',  methods=['GET'])
def serve_image(filename):
    try:
        return send_from_directory('./uploads/', filename)
    except:
        abort(404)
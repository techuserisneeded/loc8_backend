from flask import Blueprint, request, jsonify
from app.utils.helpers import token_required, superadmin_required
from app.utils.db_helper import query_db

location_bp = Blueprint('location', __name__)

@location_bp.route('/states', methods=['POST'])
@token_required
def add_state(current_user):
    data = request.get_json()
    state_name = data.get('state_name')
    zone_id = data.get('zone_id')

    if not state_name or not zone_id:
        return jsonify({'message': 'State name and zone ID are required'}), 400

    query = "INSERT INTO states (state_name, zone_id) VALUES (%s, %s)"
    args = (state_name, zone_id)
    query_db(query, args, False, True)

    return jsonify({'message': 'State added successfully'}), 201

@location_bp.route('/cities', methods=['POST'])
@token_required
def add_city(current_user):
    data = request.get_json()
    city_name = data.get('city_name')
    state_id = data.get('state_id')

    if not city_name or not state_id:
        return jsonify({'message': 'City name and state ID are required'}), 400

    query = "INSERT INTO cities (city_name, state_id) VALUES (%s, %s)"
    args = (city_name, state_id)
    query_db(query, args, False, True)

    return jsonify({'message': 'City added successfully'}), 201

@location_bp.route('/zones', methods=['GET'])
@token_required
def get_zones(current_user):
    query = "SELECT * FROM zones"
    zones = query_db(query)
    return jsonify(zones)

@location_bp.route('/states', methods=['GET'])
@token_required
def get_states(current_user):
    zone_id = request.args.get('zone_id')
    if zone_id:
        query = "SELECT * FROM states inner join zones on zones.zone_id=states.zone_id WHERE states.zone_id = %s"
        args = (zone_id,)
    else:
        query = "SELECT * FROM states inner join zones on zones.zone_id=states.zone_id"
        args = ()

    states = query_db(query, args)
    return jsonify(states)

@location_bp.route('/cities', methods=['GET'])
@token_required
def get_cities(current_user):
    state_id = request.args.get('state_id') 

    if state_id:
        query = "SELECT * FROM cities inner join states on cities.state_id=states.state_id WHERE cities.state_id = %s"
        args = (state_id,)
    else:
        query = "SELECT * FROM cities inner join states on cities.state_id=states.state_id"
        args = ()

    cities = query_db(query, args)
    return jsonify(cities)

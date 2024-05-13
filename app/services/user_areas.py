from app.utils.db_helper import query_db


def insert_user_areas(user_id, zone_id=None, state_id=None, city_id=None):
    planner_user_area_q = """
        INSERT INTO 
            user_areas( user_id, zone_id, state_id, city_id)
            values (%s, %s, %s, %s)
        """
    
    query_db(planner_user_area_q, (user_id, zone_id, state_id, city_id), False, True)
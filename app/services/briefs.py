from app.utils.db_helper import query_db
from app.utils.helpers import clean_and_lower, generate_uuid

def get_brief_details_by_brief_id (brief_id=""):
   q = """
        SELECT * FROM briefs WHERE brief_id=%s;
    """
   
   brief_data = query_db(q, (brief_id,), True)

   return brief_data


def assign_brief_to_planners(brief_id=""):
   budgets_q = """
        SELECT budget_id, zone_id, state_id, city_id FROM `brief_budgets` WHERE brief_id=%s
    """ 
   
   budgets  = query_db(budgets_q, (brief_id,))


   if budgets == None:
       return

   for budget in budgets:
        planner_q = """
            SELECT user_areas.user_id 
            FROM user_areas 
            INNER JOIN users 
                ON users.id=user_areas.user_id
            WHERE 
                    user_areas.zone_id=%s 
                AND user_areas.state_id=%s 
                AND user_areas.city_id=%s 
                AND users.role_id=1
        """

        planners = query_db(planner_q, (
            budget['zone_id'], budget['state_id'], 
            budget['city_id']
        ))

        if planners == None:
            continue

        for planner in planners:
            assigned_user_q = """
                SELECT user_id FROM assigned_budgets WHERE budget_id=%s AND user_id=%s 
            """ 

            assigned_user = query_db(assigned_user_q, (budget['budget_id'], planner['user_id']))

            if assigned_user != None:
                continue

            id = generate_uuid()

            insert_assign_q = """
                INSERT INTO `assigned_budgets`
                    (`id`, `user_id`, `budget_id`) 
                VALUES 
                    (%s, %s, %s)
            """
            query_db(insert_assign_q, (id, planner['user_id'], budget['budget_id']), False, True)




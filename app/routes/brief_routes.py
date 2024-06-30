from flask import Blueprint, request, jsonify, current_app, send_file
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import json
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from io import BytesIO

from app.utils.db_helper import query_db
from app.utils.helpers import token_required, generate_uuid, clean_and_lower
from app.services.briefs import get_brief_details_by_brief_id, assign_brief_to_planners
from app.constants.roles import roles

brief_bp = Blueprint('brief', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

osmo_logo_path = "./assets/Logo1.png"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@brief_bp.route('/briefs', methods=['POST'])
@token_required
def createBrief(current_user):
    data = request.form

    current_user_id = current_user['id']

    if 'brand_logo' not in request.files:
        return jsonify({'message': 'Please provide brand logo'}), 400

    # assign data
    brief_id = generate_uuid();
    category = clean_and_lower(data['category'])
    brand_name = clean_and_lower(data['brand_name'])
    target_aud = clean_and_lower(data['target_aud'])
    camp_obj = clean_and_lower(data['camp_obj'])
    med_app = clean_and_lower(data['med_app'])
    is_immediate_camp = clean_and_lower(data['is_immediate_camp'])
    start_date = data.get("start_date")
    notes = data.get('notes')

    budgets = data.get("budgets")
    budgets = json.loads(budgets)

    if notes != None or notes != "":
        notes = clean_and_lower(notes) 

    if start_date != None or start_date != "":
        start_date = clean_and_lower(start_date) 

    file = request.files['brand_logo']

    # validate data
    if is_immediate_camp == 1 and not start_date:
        return jsonify({"message" : "Campaing is immdiate and we require start date!"}) , 400
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if start_date <= datetime.now():
            return jsonify({'message': 'Start date must be a future date'}), 400

    
    filename = brief_id + secure_filename(file.filename)
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    
    try:
        query_db("START TRANSACTION", ())

        brief_insert_q = """
                INSERT INTO `briefs`
                (
                    `brief_id`, `category`, `brand_name`, `brand_logo`, 
                    `target_audience`, `campaign_obj`, `media_approach`, `is_immediate_camp`, 
                    `start_date`, `notes`, `created_by_user_id`
                ) 
            VALUES (
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s
                )
        """

        query_db(brief_insert_q, (
            brief_id, category, brand_name, filename, 
            target_aud, camp_obj, med_app, is_immediate_camp,
            start_date, notes, current_user_id
        ))

        for budget in budgets:
            zone_id = budget.get("zone_id")
            state_id = budget.get("state_id")
            city_id = budget.get("city_id")
            budget_amt = budget.get("budget")
            budget_id = generate_uuid();

            budget_insert_q = """
                INSERT INTO `brief_budgets` (`budget_id`, `brief_id`, `zone_id`, `state_id`, `city_id`, `budget`)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            query_db(budget_insert_q, (budget_id, brief_id, zone_id, state_id, city_id, budget_amt))
        
        current_app.mysql.connection.commit()

        assign_brief_to_planners(brief_id)
        
        return jsonify({'message': 'Created successfully'}), 201
    except Exception as e:
        current_app.mysql.connection.rollback()
        print(e)
        return jsonify({'message': 'Something went wrong!'}), 500

@brief_bp.route('/briefs', methods=['GET'])
@token_required
def getBriefs(current_user):
    try:
        user_id = current_user['id']

        query = ""
        args = ()

        if current_user['role_id'] == roles.get("SUPERADMIN"):
            query = """
            SELECT b.*, bb.budget_id, bb.zone_id, bb.state_id, bb.city_id, zones.zone_name, states.state_name, cities.city_name, bb.budget,
            users.first_name, users.last_name
            FROM briefs b
            INNER JOIN brief_budgets bb ON b.brief_id = bb.brief_id
            INNER JOIN zones ON bb.zone_id = zones.zone_id
            INNER JOIN states ON bb.state_id = states.state_id
            INNER JOIN cities ON bb.city_id = cities.city_id
            INNER JOIN users ON b.created_by_user_id = users.id
        """
            
        else:

            query = """
                SELECT b.*, bb.budget_id, bb.zone_id, bb.state_id, bb.city_id, zones.zone_name, states.state_name, cities.city_name, bb.budget,
                users.first_name, users.last_name
                FROM briefs b
                INNER JOIN brief_budgets bb ON b.brief_id = bb.brief_id
                INNER JOIN zones ON bb.zone_id = zones.zone_id
                INNER JOIN states ON bb.state_id = states.state_id
                INNER JOIN cities ON bb.city_id = cities.city_id
                INNER JOIN users ON b.created_by_user_id = users.id
                WHERE b.created_by_user_id = %s
            """

            args = (user_id,)
            
        briefs_with_budgets = query_db(query, args)

        if briefs_with_budgets == None: 
            return jsonify([]), 200

        briefs_data = {}

        for row in briefs_with_budgets:
            brief_id = row['brief_id']
            if brief_id not in briefs_data:
                briefs_data[brief_id] = {
                    'brief_id': brief_id,
                    'category': row['category'],
                    'brand_name': row['brand_name'],
                    'brand_logo': row['brand_logo'],
                    'campaign_obj': row['campaign_obj'],
                    'start_date': row['start_date'],
                    'status': row['status'],
                    'budgets': []
                }
            if row['budget_id'] is not None:
                budget_data = {
                    'budget_id': row['budget_id'],
                    'zone_id': row['zone_id'],
                    'state_id': row['state_id'],
                    'city_id': row['city_id'],
                    'zone_name': row['zone_name'],
                    'state_name': row['state_name'],
                    'city_name': row['city_name'],
                    'budget': row['budget']
                }
                briefs_data[brief_id]['budgets'].append(budget_data)

        briefs_list = list(briefs_data.values())

        return jsonify(briefs_list), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong!'}), 500
    
@brief_bp.route('/briefs/<brief_id>', methods=['DELETE'])
@token_required
def deleteBrief(current_user, brief_id):

    brief_data = get_brief_details_by_brief_id(brief_id)

    # only admin and owner of the brief can delete 
    if(brief_data['created_by_user_id'] != current_user['id'] and current_user['role_id'] != roles.get("SUPERADMIN")):
        return jsonify({
            'message': "You cannot delete this brief!",
        }), 401

    q = """
        DELETE FROM brief_budgets WHERE brief_id=%s
    """

    query_db(q, (brief_id,))

    q = """
        DELETE FROM briefs WHERE brief_id=%s
    """

    query_db(q, (brief_id,))

    current_app.mysql.connection.commit()

    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], brief_data['brand_logo']))

    return jsonify({"message": "Deleted Successfully!"}), 200

@brief_bp.route('/briefs/<brief_id>', methods=['GET'])
@token_required
def editBrief(current_user, brief_id):

    brief_data = get_brief_details_by_brief_id(brief_id)

    # # only admin and owner of the brief can delete 
    # if(brief_data['created_by_user_id'] != current_user['id'] and current_user['role_id'] != roles.get("SUPERADMIN")):
    #     return jsonify({
    #         'message': "You cannot edit this brief!",
    #     }), 401

    
    query = """
            SELECT bb.*, zones.zone_name, states.state_name, cities.city_name
            FROM brief_budgets bb
            INNER JOIN zones ON bb.zone_id = zones.zone_id
            INNER JOIN states ON bb.state_id = states.state_id
            INNER JOIN cities ON bb.city_id = cities.city_id
            WHERE bb.brief_id = %s
        """
    
    budgets = query_db(query, (brief_id,))

    brief_data["budgets"] = budgets

    return jsonify(brief_data), 200


@brief_bp.route('/planner', methods=['GET'])
@token_required
def getPlannerBriefs(current_user):
    user_id = current_user['id']

    assigned_brief_q = """
        SELECT b.*, bb.budget_id, bb.zone_id, bb.state_id, bb.city_id, zones.zone_name, states.state_name, cities.city_name, bb.budget,
        users.first_name, users.last_name
        FROM assigned_budgets ab
        INNER JOIN brief_budgets bb ON ab.budget_id = bb.budget_id
        INNER JOIN briefs b ON b.brief_id=bb.brief_id
        INNER JOIN zones ON bb.zone_id = zones.zone_id
        INNER JOIN states ON bb.state_id = states.state_id
        INNER JOIN cities ON bb.city_id = cities.city_id
        INNER JOIN users ON b.created_by_user_id = users.id
        WHERE 
            ab.user_id=%s
    """
    assigned_brief_args = (user_id,)

    briefs_with_budgets = query_db(assigned_brief_q, assigned_brief_args)

    if briefs_with_budgets == None: 
        return jsonify([]), 200

    briefs_data = {}

    for row in briefs_with_budgets:
        brief_id = row['brief_id']
        if brief_id not in briefs_data:
            briefs_data[brief_id] = {
                'brief_id': brief_id,
                'category': row['category'],
                'brand_name': row['brand_name'],
                'brand_logo': row['brand_logo'],
                'campaign_obj': row['campaign_obj'],
                'start_date': row['start_date'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'status': row['status'],
                'budgets': []
            }
        if row['budget_id'] is not None:
            budget_data = {
                'budget_id': row['budget_id'],
                'zone_id': row['zone_id'],
                'state_id': row['state_id'],
                'city_id': row['city_id'],
                'zone_name': row['zone_name'],
                'state_name': row['state_name'],
                'city_name': row['city_name'],
                'budget': row['budget']
            }
            briefs_data[brief_id]['budgets'].append(budget_data)

    briefs_list = list(briefs_data.values())

    return jsonify(briefs_list), 200

@brief_bp.route('/budgets/<budget_id>', methods=['GET'])
@token_required
def getBriefBudgetDetailsByBudgetId(current_user, budget_id):

    current_user_id = current_user['id']
    
    query = """
            SELECT bb.budget_id, briefs.brief_id, bb.zone_id, bb.state_id, bb.city_id, zones.zone_name, states.state_name, cities.city_name, bb.budget, ab.status 
            FROM assigned_budgets ab
            INNER JOIN brief_budgets bb ON ab.budget_id = bb.budget_id
            INNER JOIN briefs ON briefs.brief_id=bb.brief_id
            INNER JOIN zones ON bb.zone_id = zones.zone_id
            INNER JOIN states ON bb.state_id = states.state_id
            INNER JOIN cities ON bb.city_id = cities.city_id
            WHERE 
                    ab.budget_id=%s
                AND
                    ab.user_id=%s

        """
    
    video_query = """
        SELECT * FROM videofiles v
        WHERE v.zone_id=%s AND v.state_id=%s AND v.city_id=%s
    """
    
    plans_query = """
        SELECT plans.plan_id, b.* FROM plans
        INNER JOIN billboards b ON b.id=plans.billboard_id 
        WHERE budget_id=%s AND user_id=%s
        ORDER BY created_at ASC
    """

    budget = query_db(query, (budget_id, current_user_id), True)

    if budget == None:
        return jsonify({}), 200

    plans = query_db(plans_query, (budget['budget_id'], current_user_id))
    videos = query_db(video_query, (budget['zone_id'], budget['state_id'], budget['city_id']))

    video_data = []

    if videos:
        for video in videos:
            q = """
                SELECT * FROM video_coordinates
                WHERE video_id=%s
            """

            args = (video['video_id'],)

            video_coords = query_db(q, args)

            if video_coords:
                video['coordinates'] = video_coords
            else:
                video['coordinates'] = []

            video_data.append(video)

    return jsonify({'budget':  budget, 'videos': video_data, 'plans': plans }), 200

@brief_bp.route('/briefs/<brief_id>/planner', methods=['GET'])
@token_required
def getBriefDetailsForPlanner(current_user, brief_id):

    brief_data = get_brief_details_by_brief_id(brief_id)
    user_id = current_user['id']
    
    query = """
            SELECT bb.budget_id, bb.zone_id, bb.state_id, bb.city_id, zones.zone_name, states.state_name, cities.city_name, bb.budget FROM assigned_budgets ab
            INNER JOIN brief_budgets bb ON ab.budget_id = bb.budget_id
            INNER JOIN zones ON bb.zone_id = zones.zone_id
            INNER JOIN states ON bb.state_id = states.state_id
            INNER JOIN cities ON bb.city_id = cities.city_id
            WHERE bb.brief_id=%s
                AND
                ab.user_id=%s
        """
    
    budgets = query_db(query, (brief_id, user_id))

    brief_data["budgets"] = budgets

    return jsonify(brief_data), 200

@brief_bp.route('/budgets/<budget_id>/<brief_id>/finish', methods=['PUT'])
@token_required
def finish_budget_plan(current_user, budget_id, brief_id):
    
    user_id = current_user['id']

    query = """
        UPDATE assigned_budgets
            SET status=2
        WHERE 
                budget_id=%s
            AND
                user_id=%s
    """

    query_db(query, (budget_id, user_id), True, True)

    query =  """
        SELECT count(budget_id) 
        FROM brief_budgets
        WHERE
            brief_id=%s
    """


    response = query_db(query, (brief_id,), True)

    # no of budget in the brief
    n_budgets_in_brief = response['count(budget_id)']

    query =  """
        SELECT count(assigned_budgets.budget_id)
        FROM assigned_budgets
        INNER JOIN brief_budgets
            ON brief_budgets.budget_id=assigned_budgets.budget_id
		WHERE
        		brief_budgets.brief_id=%s
            AND
            	assigned_budgets.status=2;
    """

    response = query_db(query, (brief_id,), True)

    # no of budget completed
    n_budgets_finished = response['count(assigned_budgets.budget_id)']

    if(n_budgets_in_brief == n_budgets_finished):
        query = """
            UPDATE briefs
                SET status=1
            WHERE
                brief_id=%s
        """

        query_db(query, (brief_id,), True, True)


    return jsonify({'message': "Plan updated!"})

@brief_bp.route("/briefs/<brief_id>/plans")
@token_required
def get_plans_by_brief_id(current_user, brief_id):

    q = """
            SELECT p.*, z.zone_name, s.state_name, c.city_name FROM plans p
            INNER JOIN brief_budgets bb 
            ON p.budget_id=bb.budget_id
            INNER JOIN zones z
            ON z.zone_id=bb.zone_id
            INNER JOIN states s
            ON s.state_id=bb.state_id
            INNER JOIN cities c
            ON c.city_id=bb.city_id
            WHERE p.brief_id=%s
        """
    args=(brief_id,)

    plan_details = query_db(q, args)

    if plan_details == None:
       return jsonify([]), 200
   
    return jsonify(plan_details), 200


@brief_bp.route('/briefs/<brief_id>/download', methods=['GET'])
@token_required
def download_plan(current_user, brief_id):
    
    user_id = current_user['id']

    brief_details = get_brief_details_by_brief_id(brief_id)

    query = """
        SELECT bb.*, zones.zone_name, states.state_name, cities.city_name
        FROM brief_budgets bb
        INNER JOIN zones ON bb.zone_id = zones.zone_id
        INNER JOIN states ON bb.state_id = states.state_id
        INNER JOIN cities ON bb.city_id = cities.city_id
        WHERE bb.brief_id = %s
    """

    budgets = query_db(query, (brief_id,))
    
    brand_logo_path = current_app.config['UPLOAD_FOLDER'] +"/"+ brief_details['brand_logo']

    prs = Presentation()

    # slide dimensions for widescreen (16:9)
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    # slide with blank layout
    blank_slide_layout = prs.slide_layouts[6]
    intro_slide = prs.slides.add_slide(blank_slide_layout)

    intro_slide = create_intro_slide(intro_slide, brand_logo_path, )

    for budget in budgets:
        area_slide = prs.slides.add_slide(blank_slide_layout)

        area_slide = create_area_slide(area_slide, brand_logo_path, budget['zone_name'], budget['state_name'], budget['city_name'])

        query = """
            SELECT * FROM plans
            WHERE budget_id=%s
        """

        plans = query_db(query, (budget['budget_id'],))

        for plan in plans:
            location  = plan['location']
            size_text = "Size: {}×{}".format(plan['height'], plan['width'])

            plan_slide = prs.slides.add_slide(blank_slide_layout)

            # heading
            title_shape = plan_slide.shapes.add_textbox(Inches(0.2), Inches(0.2), Inches(4.8), Inches(0.8))
            title_text_frame = title_shape.text_frame
            title_text_frame.text = "{}   {}".format(location, size_text)
            title_text_frame.word_wrap = True
            p = title_text_frame.paragraphs[0]
            p.font.size = Inches(0.23)
            p.font.color.rgb = RGBColor(255, 165, 0)

            title_shape.fill.solid()
            title_shape.fill.fore_color.rgb = RGBColor(0, 0, 255)

            # brand logo
            image_path = brand_logo_path
            left_inch = Inches(8.5)
            top_inch = Inches(0.2)
            width_inch = Inches(2.5)
            height_inch = Inches(1)
            plan_slide.shapes.add_picture(image_path, left_inch, top_inch, width_inch, height_inch)

            # Add osmo logo
            image_path = osmo_logo_path
            left_inch = Inches(11.3)
            top_inch = Inches(0.1)
            width_inch = Inches(2)
            height_inch = Inches(1)
            plan_slide.shapes.add_picture(image_path, left_inch, top_inch, width_inch, height_inch)

            site_image_path = current_app.config['UPLOAD_FOLDER'] +"/"+ plan['site_image']
            map_image_path = current_app.config['UPLOAD_FOLDER'] +"/"+ plan['map_image']

            # site image
            left_inch = Inches(1)
            top_inch = Inches(1.2)
            width_inch = Inches(11)
            height_inch = Inches(6.2)
            plan_slide.shapes.add_picture(site_image_path, left_inch, top_inch, width_inch, height_inch)

            # Map Image
            left_inch = Inches(9)
            top_inch = Inches(5)
            width_inch = Inches(4.2)
            height_inch = Inches(2.5)
            plan_slide.shapes.add_picture(map_image_path, left_inch, top_inch, width_inch, height_inch)




    # creating thank you slide-
    thank_u_slide = prs.slides.add_slide(blank_slide_layout)

    # add logo
    image_path = osmo_logo_path
    left_inch = Inches(5.5)
    top_inch = Inches(2.5)
    width_inch = Inches(2.5)
    height_inch = Inches(1.5)
    thank_u_slide.shapes.add_picture(image_path, left_inch, top_inch, width_inch, height_inch)

    # add title
    title_shape = thank_u_slide.shapes.add_textbox(Inches(4.1), Inches(4), Inches(4.5), Inches(1))
    title_text_frame = title_shape.text_frame
    title_text_frame.text = "Let's create something irresistible"
    p = title_text_frame.paragraphs[0]
    p.font.size = Inches(0.4)
    p.font.color.rgb = RGBColor(128, 128, 128)

    presentation_bytes = BytesIO()
    prs.save(presentation_bytes)
    presentation_bytes.seek(0)


    return send_file(
        presentation_bytes,
        as_attachment=True,
        download_name="presentation.pptx",
        mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )


def create_intro_slide(intro_slide, brand_logo_path):
    
    # brand logo
    image_path = brand_logo_path
    left_inch = Inches(5.5)
    top_inch = Inches(1.3)
    width_inch = Inches(2.5)
    height_inch = Inches(1.5)
    intro_slide.shapes.add_picture(image_path, left_inch, top_inch, width_inch, height_inch)

    # heading
    title_shape = intro_slide.shapes.add_textbox(Inches(4.5), Inches(3), Inches(4.5), Inches(1))
    title_text_frame = title_shape.text_frame
    title_text_frame.text = "On Street OOH"
    p = title_text_frame.paragraphs[0]
    p.font.size = Inches(0.7)
    p.font.color.rgb = RGBColor(0, 0, 255)

    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = RGBColor(255, 165, 0)

    title_shape = intro_slide.shapes.add_textbox(Inches(3.8), Inches(4.2), Inches(5.5), Inches(1))
    title_text_frame = title_shape.text_frame
    title_text_frame.text = "Recommendation"
    p = title_text_frame.paragraphs[0]
    p.font.size = Inches(0.7)
    p.font.color.rgb = RGBColor(0, 0, 255)

    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = RGBColor(255, 165, 0)

    # Add osmo logo
    image_path = osmo_logo_path
    left_inch = Inches(5.7)
    top_inch = Inches(5.2)
    width_inch = Inches(2)
    height_inch = Inches(1.3)
    intro_slide.shapes.add_picture(image_path, left_inch, top_inch, width_inch, height_inch)

    return intro_slide

def create_area_slide(intro_slide, brand_logo_path, zone="", state="", city=""):
    
    # brand logo
    image_path = brand_logo_path
    left_inch = Inches(5.5)
    top_inch = Inches(1.3)
    width_inch = Inches(2.5)
    height_inch = Inches(1.5)
    intro_slide.shapes.add_picture(image_path, left_inch, top_inch, width_inch, height_inch)

    areas = [zone, state, city]
    top = 3

    for area in areas:
        # heading
        title_shape = intro_slide.shapes.add_textbox(Inches(4.5), Inches(top), Inches(4.5), Inches(0.8))
        title_text_frame = title_shape.text_frame
        title_text_frame.text = area
        p = title_text_frame.paragraphs[0]
        p.font.size = Inches(0.4)
        p.font.color.rgb = RGBColor(0, 0, 255)

        title_shape.fill.solid()
        title_shape.fill.fore_color.rgb = RGBColor(255, 165, 0)

        top = top + 0.8

    # Add osmo logo
    image_path = osmo_logo_path
    left_inch = Inches(5.7)
    top_inch = Inches(5.2)
    width_inch = Inches(2)
    height_inch = Inches(1.3)
    intro_slide.shapes.add_picture(image_path, left_inch, top_inch, width_inch, height_inch)

    return intro_slide

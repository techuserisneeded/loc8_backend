from app.utils.db_helper import query_db
from app.utils.helpers import clean_and_lower, generate_uuid
import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
import os
from PIL import Image
def send_email(to_email, subject, message):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    smtp_user =  os.getenv('SMTP_USER')
    smtp_password =  os.getenv('SMTP_PASSWORD')

   
    msg = EmailMessage()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject

    files = ["./assets/Logo1.png", './assets/image.png']
    file_name = 'Osmo_logo'
    for file in files: 
        with open(file,'rb') as f:
            file_data = f.read()
            image = Image.open(file)
            file_type = image.format
            file_name = f.name
        
        msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
    
    msg.attach(MIMEText(message, 'html'))
    

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()

        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {str(e)}"


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
            SELECT user_areas.user_id,
            users.email 
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
                
                
        html_message = """
        <html>
        <head></head>
        <body>
            <h3>You are assigned a brief. Login to <a href="http://loc8.tech"> know more</a>.</h3>
        </body>
        </html>
        """
        
        for planner in planners:    
            send_email(planner['email'], "Assignment", html_message)
        
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




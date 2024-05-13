from flask import current_app
from flask_mysqldb import MySQL

def init_db(app):
    mysql = MySQL(app)
    return mysql

def query_db(query, args=(), one=False, commit=False):
    cursor = current_app.mysql.connection.cursor()
    cursor.execute(query, args)

    if commit:
        current_app.mysql.connection.commit()
        return cursor.lastrowid 

    columns = [column[0] for column in cursor.description] if cursor.description else None

    if not columns:
        cursor.close()
        return None

    data = cursor.fetchone() if one else cursor.fetchall()
    cursor.close()

    if not data:
        return None

    result = [dict(zip(columns, row)) for row in data] if not one else dict(zip(columns, data))
    return result

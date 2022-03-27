from models.db import get_cursor
from flask import flash

# get user by id
# Sophia
def get_user(id):
    cur = get_cursor()
    cur.execute("SELECT id,full_name,office,contact,admin_access,user_status FROM user WHERE id=%s;",(id,))
    rows = cur.fetchall()
    return rows[0] if len(rows)>0 else None

# get all active users
# Sophia
def get_all_users():
    cursor=get_cursor()
    cursor.execute("SELECT id,full_name,office,contact,admin_access FROM user where user_status='active';")   
    return cursor.fetchall()


#get user id
def id_num(id):
    cur = get_cursor()
    cur.execute("SELECT id, full_name FROM user WHERE id = %s;", (id,))
    id_number = cur.fetchone()
    return id_number





        
    
    



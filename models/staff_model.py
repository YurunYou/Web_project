from flask import flash
from models.db import get_cursor


# create a new staff
def create_staff(form):
    cursor = get_cursor()
    full_name = form.get('full_name')
    office = form.get('office')
    contact = form.get('contact')
    admin_access = form.get('admin_access')
    user_status = form.get('user_status')

    cursor.execute(
        'INSERT INTO user (full_name, office, contact, admin_access, user_status) VALUES (%s, %s, %s, %s, %s);',
        (full_name, office, contact, admin_access, user_status))


# Validate form request for staff
def validate_staff(form):
    result = True
    if form.get('full_name') == '':
        flash('Name is required!', category='error')
        result = False
    if form.get('office') == '':
        flash('office site is required', category='error')
        result = False
    if form.get('contact') == '':
        flash('Phone number is required', category='error')
        result = False
    return result


# get staff by id
# Sophia
def get_staff(id):
    cur = get_cursor()
    cur.execute("SELECT id,full_name,office,contact,admin_access,user_status FROM user WHERE id=%s;", (id,))
    rows = cur.fetchall()
    return rows[0] if len(rows) > 0 else None


# get staff_profile
def get_staff_profile(id):
    cur = get_cursor()
    cur.execute("SELECT full_name,office,contact FROM user WHERE id=%s;", (id,))
    rows = cur.fetchone()
    return rows


# Update a staff info from admin request
# Sophia
def update_staff(form, id):
    cursor = get_cursor()
    full_name = form.get('full_name')
    office = form.get('office')
    contact = form.get('contact')
    admin_access = 1 if form.get('admin_access') == 'on' else 0
    cursor.execute("UPDATE user SET full_name=%s,office=%s,contact=%s,admin_access=%s WHERE id=%s",
                   (full_name, office, contact, admin_access, id))
    return cursor.fetchall()


# Update a staff profile in staff page
def update_staff_profile(form, id):
    cursor = get_cursor()
    full_name = form.full_name.data
    office = form.office.data
    contact = form.contact.data
    cursor.execute("UPDATE user SET full_name=%s,office=%s,contact=%s WHERE id=%s", (full_name, office, contact, id))
    return cursor.fetchall()


# delete staff info from admin request
# Sophia
def delete_staff(id):
    cursor = get_cursor()
    user_status = 'inactive'
    cursor.execute("UPDATE user SET user_status=%s WHERE id=%s",
                   (user_status, id))
    return cursor.fetchall()

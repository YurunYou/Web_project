from flask import flash
from datetime import datetime, timedelta
from enums.device_status_enum import DeviceStatus
from models.db import get_cursor
import datetime


# create a new device
# Author: Kokila
def create_device(form):
    cursor = get_cursor()
    device_name = form.get('device_name')
    device_type = form.get('device_type')
    model = form.get('model')
    os_type = form.get('os_type')
    os_version = form.get('os_version')
    ram = form.get('ram')
    cpu = form.get('cpu')
    bit = form.get('bit')
    screen_resolution = form.get('screen_resolution')
    grade = form.get('grade')
    uuid = form.get('uuid')
    device_status = form.get('device_status')
    # device_status="Available"

    cursor.execute(
        'INSERT INTO device (device_name, device_type, model, os_type, os_version, ram, cpu, bit,'
        ' screen_resolution, grade, uuid,device_status) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
        (device_name, device_type, model, os_type, os_version, ram, cpu, bit, screen_resolution, grade,
         uuid, device_status))


# Edit device details
# Author: Kokila
def edit_device(device_id, form):
    cursor = get_cursor()
    device_name = form.get('device_name')
    os_version = form.get('os_version')
    ram = form.get('ram')
    screen_resolution = form.get('screen_resolution')
    grade = form.get('grade')
    device_status = form.get('device_status')

    cursor.execute(
        "UPDATE device Set device_name= %s, os_version= %s, ram= %s, screen_resolution= %s, grade= %s,device_status= %s WHERE id=%s",
        (device_name, os_version, ram, screen_resolution, grade, device_status, device_id,))


# Assign a device to a user in assignment table
# Author: Kokila
def assign_device(device_id, user_id, estimate_return_date):
    cursor = get_cursor()
    device_id = device_id
    user_id = user_id
    borrow_date = datetime.date.today().strftime('%Y-%m-%d')
    if estimate_return_date == '':
        due_date = (datetime.date.today() + (timedelta(days=14))).strftime('%Y-%m-%d')
    else:
        due_date = estimate_return_date

    cursor.execute(
        'INSERT INTO assignment (device_id, user_id, borrow_date, due_date) VALUES(%s, %s, %s, %s);',
        (device_id, user_id, borrow_date, due_date))


# soft delete a device by updating device status = 'deleted'
# Author: Kokila
def delete_device(device_id):
    cursor = get_cursor()
    id = device_id
    device_status = "deleted"
    cursor.execute("Update device Set device_status= %s WHERE id=%s", (device_status, id,))


# Assign device by updating device status = 'unavailable'
# Author: Kokila
def unavailable_device(device_id):
    cursor = get_cursor()
    id = device_id
    device_status = "unavailable"
    cursor.execute("Update device Set device_status= %s WHERE id=%s", (device_status, id,))


# Get selected device
# Author: Kokila
def get_device(device_id):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM device where id=%s", (device_id,))
    return cursor.fetchone()


# Validate number of devices with user
#  Author: Kokila
def validate_device_count_user(user_id):
    result = True
    cursor = get_cursor()
    device_status = "broken"
    cursor.execute("SELECT count(assignment.device_id) as TotalDevices FROM assignment INNER JOIN device ON "
                   "assignment.device_id = device.id WHERE assignment.user_id = %s AND device.device_status != %s AND "
                   "assignment.return_date is NULL", (user_id, device_status,))
    TotalDevices = cursor.fetchone()[0]
    print(TotalDevices)
    if int(TotalDevices) >= 3:
        flash('Borrowing limit is already reached (3), please return a device first!', category='error')
        result = False
    return result


# Validate form request for device
# Author: Kokila
def validate_device(form):
    result = True
    if form.get('device_name') == '':
        flash('Device Name is required!', category='error')
        result = False
    if form.get('device_type') == '':
        flash('Device type is required', category='error')
        result = False
    if form.get('model') == '':
        flash('Model is required', category='error')
        result = False

    if form.get('os_type') == '':
        flash('OS Type is required', category='error')
        result = False
    return result


# Get all devices
# Sophia
def get_devices():
    sql = '''
        SELECT * FROM (
            SELECT device.id, device.device_name, device.device_type, device.os_type, device.cpu, device.ram, device.device_status, '' as user_name, '' as due_date
            FROM device WHERE device_status IN ('{0}', '{1}')
            UNION 
            SELECT device.id, device.device_name, device.device_type, device.os_type, device.cpu, device.ram, device.device_status, `user`.full_name as user_name, `assignment`.due_date  
            FROM device
            INNER JOIN `assignment` ON `assignment`.device_id =device.id
            INNER JOIN `user` ON `assignment`.user_id =`user`.id
            WHERE device.device_status='{2}' AND `assignment`.return_date IS NULL
        ) t ORDER BY t.device_status desc;
    '''
    sql = sql.format(DeviceStatus.Available.value, DeviceStatus.Broken.value, DeviceStatus.Unavailable.value)
    cursor = get_cursor()
    cursor.execute(sql)
    return cursor.fetchall()


# get all borrowed devices by user_id
# Sophia
def get_my_devices(user_id):
    cursor = get_cursor()
    device_status = "broken"
    cursor.execute('SELECT device.id,device.device_name, device.device_type,device.model,assignment.due_date \
                   FROM device join assignment on device.id=assignment.device_id \
                   WHERE device.device_status != %s AND assignment.return_date IS NULL AND assignment.user_id=%s;',
                   (device_status, user_id,))
    rows = cursor.fetchall()
    return rows


# get devie_id and delete device
def get_unassign(device_id):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM assignment where device_id = %s", (device_id,))
    return cursor.fetchone()


# update device to available
def unassign_device(device_id):
    cursor = get_cursor()
    device_status = "available"
    cursor.execute("Update device Set device_status = %s WHERE id = %s", (device_status, device_id,))


# add the broken device information to the broken_device table.
def report_broken_device(device_id, user_id, comments):
    cursor = get_cursor()
    device_id = device_id
    user_id = user_id
    report_date = datetime.date.today().strftime('%Y-%m-%d')
    comments = comments

    cursor.execute(
        'INSERT INTO broken_device (device_id, user_id, report_date, comments) VALUES(%s, %s, %s, %s);',
        (device_id, user_id, report_date, comments))


# update device to broken
def broken_device(device_id):
    cursor = get_cursor()
    device_status = "broken"
    cursor.execute("UPDATE device SET device_status = %s WHERE id = %s;", (device_status, device_id,))


# update return device time
def update_return_date(device_id):
    cursor = get_cursor()
    return_date = datetime.date.today().strftime('%Y-%m-%d')
    cursor.execute("UPDATE assignment SET return_date = %s  WHERE device_id = %s",
                   (return_date, device_id,))


# get RAM values for all active devices
def get_ram_list():
    cursor = get_cursor()
    cursor.execute('''SELECT DISTINCT(ram) FROM device WHERE device_status<>'deleted' AND ram IS NOT NULL AND ram<>'' 
                   ORDER BY ram;''')
    return cursor.fetchall()


# get CPU values for all active devices
def get_cpu_list():
    cursor = get_cursor()
    cursor.execute('''SELECT DISTINCT(cpu) FROM device WHERE device_status<>'deleted' AND cpu IS NOT NULL AND cpu<>'' 
                   ORDER BY cpu;''')
    return cursor.fetchall()


# search devices
def search_devices(search_form):
    device_type = search_form.get('device_type')
    os_type = search_form.get('os_type')
    ram = search_form.get('ram')
    cpu = search_form.get('cpu')
    search = search_form.get('search')

    values = ()

    sql = '''
            SELECT * FROM (
                SELECT device.id, device.device_name, device.device_type, device.os_type, device.cpu, device.ram, device.device_status, '' as user_name, '' as due_date
                FROM device WHERE device_status IN ('available', 'broken')
                UNION 
                SELECT device.id, device.device_name, device.device_type, device.os_type, device.cpu, device.ram, device.device_status, `user`.full_name as user_name, `assignment`.due_date  
                FROM device
                INNER JOIN `assignment` ON `assignment`.device_id =device.id
                INNER JOIN `user` ON `assignment`.user_id =`user`.id
                WHERE device.device_status='unavailable' AND `assignment`.return_date IS NULL
            ) t WHERE 1=1
        '''
    if device_type:
        sql += ' AND t.device_type=%s'
        values += (device_type,)
    if os_type:
        sql += ' AND t.os_type=%s'
        values += (os_type,)
    if ram:
        sql += ' AND t.ram=%s'
        values += (ram,)
    if cpu:
        sql += ' AND t.cpu=%s'
        values += (cpu,)
    if search:
        sql += " AND t.device_name LIKE %s"
        values += ("%" + search + "%",)

    sql += ' ORDER BY t.device_name;'

    cursor = get_cursor()
    cursor.execute(sql, values)
    devices = cursor.fetchall()

    return devices


# get all broken devices report
# Sophia
def broken_devices_report():
    cursor = get_cursor()
    cursor.execute(
        "SELECT device.device_name,device.device_type,device.model,broken_device.report_date,broken_device.comments from device join broken_device on device.id=broken_device.device_id;")
    return cursor.fetchall()


# get overdue devices report
# Sophia
def over_due_report():
    cursor = get_cursor()
    cursor.execute("SELECT device.device_name,device.device_type,device.model,user.full_name,user.contact,assignment.due_date  \
                   from device join assignment on device.id=assignment.device_id \
                   join user on user.id=assignment.user_id where device_status='unavailable' and return_date is Null and due_date<date(now()) order by due_date;")
    return cursor.fetchall()


# Get all device details
def get_device_details(device_id):
    device = get_device(device_id)

    if device and len(device) == 13 and device[12] == DeviceStatus.Unavailable.value:
        sql = '''
            SELECT `assignment`.user_id, user.full_name, `assignment`.due_date
            FROM device
            INNER JOIN `assignment` ON `assignment`.device_id=device.id
            INNER JOIN user ON user.id=`assignment`.user_id
            WHERE device.id=%s AND `assignment`.return_date IS NULL
        '''
        cursor = get_cursor()
        cursor.execute(sql, (device_id,))
        device += cursor.fetchone()

    return device


# get most popular device
def most_popular_report():
    cursor = get_cursor()
    cursor.execute("SELECT device.device_name, COUNT(assignment.device_id) AS Device_borrow_times, device.device_type, device.model, device.os_version, device.os_type\
                    FROM device\
                    INNER JOIN assignment ON device.id = assignment.device_id\
                    GROUP BY assignment.device_id\
                    ORDER BY Device_borrow_times DESC")
    return cursor.fetchall()

from site import USER_SITE
from flask import Blueprint, render_template
from flask import Flask, url_for, session, flash, redirect, request

from enums.device_status_enum import DeviceStatus
from enums.device_type_enum import DeviceType
from enums.os_type_enum import OSType
from enums.device_grade_enum import DeviceGrade
from models.device_model import create_device, edit_device, validate_device, get_devices, delete_device, get_device, \
    get_ram_list, \
    get_cpu_list, search_devices, broken_devices_report, over_due_report, get_device_details, most_popular_report, \
    assign_device, unavailable_device, validate_device_count_user, get_unassign, unassign_device, update_return_date

from models.staff_model import create_staff, validate_staff, get_staff, update_staff, delete_staff

from models.user_model import get_all_users
import datetime
from models.db import get_cursor

admin_module = Blueprint('admin_module', __name__)

app = Flask(__name__)
if __name__ == "__main__":
    app.run()


# admin dashboard page
@admin_module.route("/admin/dashboard")
def admin_dashboard():
    return render_template('admin/dashboard/dashboard.html')


# Admin device index and save
@admin_module.route("/admin/device", methods=['GET', 'POST'])
def admin_device():
    if request.method == 'POST':
        form = request.form
        if not validate_device(form):
            session['device_form'] = form
            return redirect(url_for('admin_module.admin_new_device'))
        create_device(form)
        flash('Device Created!', category='success')
        return redirect(url_for('admin_module.admin_device'))

    search_form = session.get('search_form')
    if search_form:
        devices = session.get('search_device_result')
        session.pop('search_device_result')
        session.pop('search_form')
    else:
        devices = get_devices()

    ram_list = get_ram_list()
    cpu_list = get_cpu_list()

    return render_template('admin/device/device.html',
                           devices=devices,
                           device_types=DeviceType,
                           os_types=OSType,
                           ram_list=ram_list,
                           cpu_list=cpu_list,
                           search_form=search_form)


# Admin create device page
@admin_module.route("/admin/device/create", methods=['GET'])
def admin_new_device():
    form = session.get('device_form')
    if form is not None:
        session.pop('device_form')
    return render_template('admin/device/create_device.html', form=form, DeviceType=DeviceType,
                           DeviceStatus=DeviceStatus,DeviceGrade=DeviceGrade)


# Admin edit device page
@admin_module.route("/admin/device/<int:device_id>/edit", methods=['GET', 'POST'])
def admin_edit_device(device_id):
    if request.method == 'POST':
        form = request.form
        if not validate_device(form):
            session['device_form'] = form
            return redirect(url_for('admin_module.admin_edit_device', device_id=device_id))
        edit_device(device_id, form)
        flash('Device Updated!', category='success')
        return redirect(url_for('admin_module.admin_device'))
    else:
        device = get_device(device_id)
        id = device_id
        return render_template('admin/device/edit_device.html', id=id, device=device, DeviceStatus=DeviceStatus,DeviceGrade=DeviceGrade)


# Admin delete device page
@admin_module.route("/admin/device/<int:device_id>/delete", methods=['GET', 'POST'])
def admin_delete_device(device_id):
    if request.method == 'POST':
        delete_device(device_id)
        flash('Device Deleted!', category='success')
        return redirect(url_for('admin_module.admin_device'))
    else:
        device = get_device(device_id)
        id = device_id

        return render_template('admin/device/delete_device.html', id=id, device=device)


# Admin create index staff to save
@admin_module.route("/admin/staff", methods=['GET', 'POST'])
def admin_staff():
    if request.method == 'POST':
        form = request.form
        if not validate_staff(form):
            session['staff_form'] = form
            return redirect(url_for('admin_module.admin_create_staff'))
        create_staff(form)
        # flash_success('New staff has been added successfully')
        flash('Staff Created!', category='success')
        return redirect(url_for('admin_module.admin_staff'))


    users = get_all_users()
    return render_template('admin/staff/admin_staff.html', users = users)


# admin create the staff.
@admin_module.route("/admin/staff/create_staff", methods=['GET', 'POST'])
def admin_create_staff():
    form = session.get('staff_form')
    if form is not None:
        session.pop('staff_form')
    return render_template('admin/staff/create_staff.html', form=form)


# admin search device
@admin_module.route("/admin/device/search", methods=['POST'])
def admin_search_device():
    search_device_result = search_devices(request.form)
    session['search_form'] = request.form
    session['search_device_result'] = search_device_result

    return redirect(url_for('admin_module.admin_device'))


# admin update staff info and contact
# Sophia
@admin_module.route("/admin/staff/<int:id>/edit", methods=['GET', 'POST'])
def admin_edit_staff(id):
    if request.method == 'GET':
        staff = get_staff(id)
        if staff is not None:
            form = session.get('staff_form')
            if form is not None:
                session.pop('staff_form')
            return render_template('admin/staff/update_staff.html', staff=staff, form=form)
    else:
        staff = get_staff(id)
        update_staff(request.form, id)
        flash(f'staff {staff[1]} has been updated successsfully', category='success')
        return redirect(url_for('admin_module.admin_staff'))


# admin run broken devices report
# Sophia
@admin_module.route("/admin/report/broken_devices", methods=["GET"])
def admin_report_broken():
    devices = broken_devices_report()
    return render_template('admin/report/broken_devices.html', devices=devices)


# admin run overdue report
# Sophia
@admin_module.route("/admin/report/overdue", methods=["GET"])
def admin_report_overdue():
    devices = over_due_report()
    return render_template('admin/report/overdue.html', devices=devices)


# Admin view device details page
@admin_module.route("/admin/device/<int:device_id>/")
def admin_view_device(device_id):
    device = get_device_details(device_id)

    return render_template('admin/device/device_details.html', device=device)


# admin most popular devices report
@admin_module.route("/admin/report/most_popular", methods=["GET"])
def most_popular_device():
    devices = most_popular_report()
    return render_template('admin/report/most_popular.html', devices=devices)


# admin assign device page
@admin_module.route("/admin/device/<int:device_id>/assign", methods=['GET', 'POST'])
def admin_assign_device(device_id):
    if request.method == 'POST':
        form = request.form
        user_id = form.get('user')
        estimate_return_date = form.get('estimate_return_date')
        if not validate_device_count_user(user_id):
            return redirect(url_for('admin_module.admin_assign_device', device_id=device_id))
        assign_device(device_id, user_id, estimate_return_date)
        unavailable_device(device_id)
        flash('Device Assigned!', category='success')
        return redirect(url_for('admin_module.admin_device'))
    else:
        device = get_device(device_id)
        id = device_id
        now = datetime.date.today().strftime('%Y-%m-%d')
        users = get_all_users()
        return render_template('admin/device/assign_device.html', id=id, device=device, mindate=now, users=users)


# admin unassign device
@admin_module.route("/admin/device/<int:device_id>/unassign", methods=['GET', 'POST'])
def admin_unassign_device(device_id):
    get_unassign(device_id)
    unassign_device(device_id)
    update_return_date(device_id)
    flash('Device Unassigned!', category='success')
    return redirect(url_for('admin_module.admin_device'))


# Admin delete staff   
# Sophia  
@admin_module.route("/admin/staff/<int:id>/delete", methods=['POST'])
def admin_delete_staff(id):
    cursor = get_cursor()
    cursor.execute("SELECT count(*) from assignment where user_id=%s and return_date is Null;",(id,))
    unreturn = cursor.fetchone()[0]
    cursor.execute("Select full_name from user where id=%s;",(id,))
    user_name =cursor.fetchone()[0]
    if unreturn > 0:
        flash(f'Staff {user_name} has unreturned devices, please return devices first',category = 'error')
    else:
        delete_staff(id)
        flash(f'Staff {user_name} has been deleted successsfully', category='success')
    return redirect(url_for('admin_module.admin_staff'))


# Admin switch to staff
@admin_module.route("/admin/switch", methods=['GET'])
def admin_switch_staff():
    return redirect("/staff/home")

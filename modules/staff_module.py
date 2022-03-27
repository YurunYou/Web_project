from flask import Blueprint, flash, render_template, request, session, redirect, url_for

from enums.device_type_enum import DeviceType
from enums.os_type_enum import OSType
from models.device_model import get_my_devices, get_devices, unassign_device, get_unassign, \
    update_return_date, get_device, validate_device_count_user, assign_device, unavailable_device, broken_device, \
    report_broken_device, get_device_details, search_devices, get_ram_list, get_cpu_list
from models.staff_model import get_staff_profile, update_staff_profile
import datetime
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired

staff_module = Blueprint('staff_module', __name__)


class CommentsForm(FlaskForm):
    comments = TextAreaField("Please Enter Your Comments:", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UserFrom(FlaskForm):
    full_name = StringField("Full name", validators=[DataRequired()])
    office = SelectField('Office', validators=[DataRequired()], choices=["A", "B"])
    contact = StringField('Contact', validators=[DataRequired()])
    submit = SubmitField("Submit")


# staff login to see all onloan devices, alert to remind overdue devices
@staff_module.route("/staff/home", methods=['GET', 'POST'])
def staff_device():
    user = session['current_user']
    user_id = user[0]
    devices = get_my_devices(user_id)
    for device in devices:
        now = datetime.date.today().strftime('%Y-%m-%d')
        due_date = str(device[4])
        if now > due_date:
            flash(f"IMPORTANT! Please Return The Device: {device[1]}!! It should be returned before {device[4]}!!",
                  category='error')
    return render_template('staff/home/home.html', devices=devices, user=user)


# staff view all devices
@staff_module.route("/staff/device", methods=['GET', 'POST'])
def staff_all_device():
    search_form = session.get('search_form')
    if search_form:
        devices = session.get('search_device_result')
        session.pop('search_device_result')
        session.pop('search_form')
    else:
        devices = get_devices()

    ram_list = get_ram_list()
    cpu_list = get_cpu_list()

    return render_template('staff/device/device.html',
                           devices=devices,
                           device_types=DeviceType,
                           os_types=OSType,
                           ram_list=ram_list,
                           cpu_list=cpu_list,
                           search_form=search_form)


# staff update profile
@staff_module.route("/staff/profile", methods=['GET', 'POST'])
def update_profile_staff():
    user = session['current_user']
    id = user[0]
    form = UserFrom()
    get_profile = get_staff_profile(id)
    full_name = form.full_name.data
    office = form.office.data
    contact = form.contact.data
    if form.validate_on_submit():
        update_staff_profile(form, id)
        flash('Update Profile Success!', category="success")
        return redirect(url_for("staff_module.staff_device"))
    form.full_name.data = get_profile[0]
    form.office.data = get_profile[1]
    form.contact.data = get_profile[2]
    return render_template("staff/profile/staff_profile.html", id=id, form=form, full_name=full_name, office=office,
                           contact=contact)


# staff unassign device
@staff_module.route("/staff/device/<int:device_id>", methods=['GET', 'POST'])
def staff_unassign_device(device_id):
    get_unassign(device_id)
    unassign_device(device_id)
    update_return_date(device_id)
    flash('Device Unassigned!', category='success')
    return redirect(url_for('staff_module.staff_device'))


# staff report broken device
@staff_module.route("/staff/device/<int:user_id>/<int:device_id>/broken", methods=['GET', 'POST'])
def broken_device_report(user_id, device_id):
    user = user_id
    device = device_id
    comments = None
    form = CommentsForm()
    if form.validate_on_submit():
        comments = form.comments.data
        form.comments.data = ''
        report_broken_device(device_id, user_id, comments)
        broken_device(device_id)
        flash('Report success!', category="success")
        return redirect(url_for("staff_module.staff_device"))

    return render_template("staff/device/report_device.html", comments=comments, form=form, device=device, user=user)


# Staff assign device page
@staff_module.route("/staff/device/<int:device_id>/assign", methods=['GET', 'POST'])
def staff_assign_device(device_id):
    user = session['current_user']
    user_id = user[0]
    if request.method == 'POST':
        form = request.form
        estimate_return_date = form.get('estimate_return_date')
        if not validate_device_count_user(user_id):
            return redirect(url_for('staff_module.staff_device'))
        assign_device(device_id, user_id, estimate_return_date)
        unavailable_device(device_id)
        flash('Device Assigned!', category='success')
        return redirect(url_for('staff_module.staff_device'))
    else:
        device = get_device(device_id)
        id = device_id
        now = datetime.date.today().strftime('%Y-%m-%d')
        return render_template('staff/device/assign_device.html', id=id, device=device, mindate=now)


# Staff view device details page
@staff_module.route("/staff/device/<int:device_id>/details")
def staff_view_device(device_id):
    device = get_device_details(device_id)

    return render_template('staff/device/device_details.html', device=device)


# Staff search device
@staff_module.route("/staff/device/search", methods=['POST'])
def staff_search_device():
    search_device_result = search_devices(request.form)
    session['search_form'] = request.form
    session['search_device_result'] = search_device_result

    return redirect(url_for('staff_module.staff_all_device'))


# Staff switch to admin
@staff_module.route("/staff/switch", methods=['GET'])
def staff_switch_admin():
    return redirect("/admin/device")
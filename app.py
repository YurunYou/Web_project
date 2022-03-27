from datetime import datetime

from flask import Flask
from flask import session, abort
import config
from modules.admin_module import admin_module
from modules.staff_module import staff_module
from models.db import get_cursor
from models.user_model import get_user
from flask import render_template
from flask import request
from flask import redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = config.app_secret
app.register_blueprint(admin_module)
app.register_blueprint(staff_module)


@app.template_filter()
def format_nz_date(value):
    if value:
        datetime_obj = datetime.strptime(str(value), '%Y-%m-%d')
        return datetime_obj.strftime('%d/%m/%Y')
    return value


# login page
@app.route("/")
def home():
    cur = get_cursor()
    cur.execute('select * from user where user_status="Active" order by full_name ;')
    users = cur.fetchall()  # pass result to a variable#
    return render_template('login.html', users=users)  # pass parameter to the home.html page#


# login redirect
@app.route("/login", methods=['POST'])
def login():
    user_id = request.form.get('user_id')
    user = get_user(user_id)
    if user:
        session['current_user'] = user
        if user[4] == 1:
            return redirect("/admin/device")
        else:
            return redirect("/staff/home")
    else:
        abort(404)


# logout
@app.route("/logout", methods=['GET'])
def logout():
    if session['current_user']:
        session.pop('current_user')

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

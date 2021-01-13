from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app, session
from werkzeug.utils import secure_filename
from hypermarket.admin.forms import LoginForm
from hypermarket.login_required import login_required
from cryptography.fernet import Fernet
import os
import json

admin_bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


# this function load allowed admin's details.
def get_user_password(username):
    with open(os.path.join(os.path.dirname(__file__), 'users.json')) as file:
        users = json.load(file)

    for user in users:
        if user[0] == username:
            return user[1]


# This function check the entered user & password.
def check_authentication(username, password):
    f = Fernet(current_app.config.get('PASS_KEY'))
    password_ = get_user_password(username)
    # Encoding the password by a random bites key in configs.

    if password_ is None:
        return False

    return str(f.decrypt(bytes(password_, encoding='UTF-8')), encoding='UTF-8') == password or {
        username: password} in current_app.config.get('ADMIN')


# The below function handel all login page events.
@admin_bp.route('/login', methods=['POST', 'GET'])
def login():
    if 'user' in session:
        return redirect(url_for('admin.dashboard'))

    else:
        login_form = LoginForm()
        if request.method == 'GET':
            return render_template('admin/login.html', form=login_form)

        else:
            if login_form.validate_on_submit():
                username = login_form.username.data
                password = login_form.password.data
                if check_authentication(username, password):
                    session['user'] = username
                    return redirect(url_for('admin.dashboard'))

                else:
                    flash('نام کاریری یا رمز عبور اشتباه میباشد')
                    return render_template('admin/login.html', form=login_form)


# Simple routing function for admin dashboard page.
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')


# Simple routing function for admin product managing page.
@admin_bp.route('/product_manage')
@login_required
def product_manage():
    return render_template('admin/productM.html')


# Simple routing function for admin warehouse managing page.
@admin_bp.route('/warehouse_manage')
@login_required
def warehouse_manage():
    return render_template('admin/warehouseM.html')


# Simple routing function for admin orders managing page.
@admin_bp.route('/orders_manage')
@login_required
def orders_manage():
    return render_template('admin/ordersM.html')


# Routing function to manage inventories and prices.
@admin_bp.route('/inventory_price_manage')
@login_required
def inventory_price_manage():
    return render_template('admin/inventory_priceM.html')


# logging out of the admin section and redirect to main page of store.
@admin_bp.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    return redirect(url_for('store.home'))

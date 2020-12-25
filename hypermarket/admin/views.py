from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app, session
from werkzeug.utils import secure_filename
from hypermarket.admin.forms import LoginForm
from hypermarket.login_required import login_required
from cryptography.fernet import Fernet
import os
import json

admin_bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def get_user_password(username):
    with open(os.path.join(os.path.dirname(__file__), 'users.json')) as file:
        users = json.load(file)

    for user in users:
        if user[0] == username:
            return user[1]


def check_authentication(username, password):
    f = Fernet(current_app.config.get('PASS_KEY'))
    password_ = get_user_password(username)

    return str(f.decrypt(bytes(password_, encoding='UTF-8')), encoding='UTF-8') == password or {
        username: password} in current_app.config.get('ADMIN')


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
                    flash('نام کاریری یا رمز غبور اشتباه میباشد')
                    return render_template('admin/login.html', form=login_form)


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')


@admin_bp.route('/product_manage')
@login_required
def product_manage():
    products = [[
        'https://dkstatics-public.digikala.com/digikala-products/115604447.jpg?x-oss-process=image/resize,h_1600/quality,q_80',
        'چاي گلستان 400 گرمي', 'مواد غذايي'],
        [
            'https://dkstatics-public.digikala.com/digikala-products/115604447.jpg?x-oss-process=image/resize,h_1600/quality,q_80',
            'چاي گلستان 400 گرمي', 'مواد غذايي'],
        ['', 'چاي گلستان 400 گرمي', 'مواد غذايي']]
    return render_template('admin/productM.html', products=products)


@admin_bp.route('/warehouse_manage')
@login_required
def warehouse_manage():
    inventories = ['انبار شماره1', 'انبار شماره2', 'انبار شماره3', 'انبار شماره4']
    return render_template('admin/warehouseM.html', inventories=inventories)


@admin_bp.route('/orders_manage')
@login_required
def orders_manage():
    return render_template('admin/ordersM.html')


@admin_bp.route('/inventory_price_manage')
@login_required
def inventory_price_manage():
    return render_template('admin/inventory_priceM.html')


@admin_bp.route('/uploader', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        f = request.files['file']
        try:
            f.save("uploads/" + secure_filename(f.filename))
            return render_template('admin/upload.html')
        finally:
            return redirect(url_for('admin.product_manage'))


@admin_bp.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    return redirect(url_for('admin.login'))

from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app, session, g
from werkzeug.utils import secure_filename
from hypermarket.admin.forms import LoginForm
from hypermarket.login_required import login_required
import os
import json
from ..db import get_db
import psycopg2
import psycopg2.extras
# from cryptography.fernet import Fernet

store_bp = Blueprint('store', __name__, template_folder='templates', static_folder='static')

# def get_user_password(username):
#     with open(os.path.join(os.path.dirname(__file__), 'users.json')) as file:
#         users = json.load(file)

#     for user in users:
#         if user[0] == username:
#             return user[1]

# def check_authentication(username, password):
#     # f = Fernet(current_app.config.get('PASS_KEY'))
#     password_ = get_user_password(username)

#     return str(f.decrypt(bytes(password_, encoding='UTF-8')), encoding='UTF-8') == password or {username: password} in current_app.config.get('ADMIN')


# @store_bp.route('/login', methods=['POST', 'GET'])
# def login():
#     if 'user' in session:
#         return redirect(url_for('admin.dashboard'))

#     else:
#         login_form = LoginForm()
#         if request.method == 'GET':
#             return render_template('admin/login.html', form=login_form)

#         else:
#             if login_form.validate_on_submit():
#                 username = login_form.username.data
#                 password = login_form.password.data
#                 if check_authentication(username, password):
#                     session['user'] = username
#                     return redirect(url_for('admin.dashboard'))

#                 else:
#                     flash('نام کاریری یا رمز غبور اشتباه میباشد')
#                     return render_template('admin/login.html', form=login_form)


@store_bp.route('/')
def home():
    # cursor.execute("SELECT * FROM category WHERE customer_id = %s", (customer_id,))
    # g.customer = cursor.fetchone()
    # print(g.customer)
    db = get_db()
    with db:
        # with db.cursor() as cursor:
        #     cursor.execute("""select category_id from category where parent_group=0 """)
        #     child_group = [i[0] for i in cursor.fetchall()]
        
        with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute("select category_name,category_id from category where parent_group=0")
            categories = [dict(row) for row in cursor.fetchall()]
            # print(categories)
            total_product = {}

            for x in categories:
                cursor.execute(f"""select DISTINCT ON (product_name) product_name, product_ware.product_id, price, category_name, image_link from product
                                    join category on product.category_id=category.category_id
                                    join product_ware on product.id=product_ware.product_id
                                    where parent_group={x['category_id']}
                                    order by  product_name, product_date desc, price asc
                                    limit 4;""")
                each_product = [dict(row) for row in cursor.fetchall()]        
                total_product[x['category_name']] = each_product

            # print(total_product.keys())    
            # print("############################",total_product)    
            
    return render_template('home.html', total_product=total_product)
    




# print(url_for('login', next='/'))
@store_bp.route('/category/?name=<category_name>')
def category_selector(category_name):
    # category from data base
    return render_template('category.html', category=category_name)


@store_bp.route('/product/<int:product_id>')
def product_selector(product_id):
    # product from database
    # product=product
    return render_template('product.html' , id=product_id )


@store_bp.route('/cart')
def cart_creation():
    #****************************
    return render_template('cart.html')


@store_bp.route('/cart/approve')
def cart_approve_function():
    return render_template('cart_approve.html')

    # if request.method == 'POST':
    #     f = request.files['file']
    #     try:
    #         f.save("uploads/" + secure_filename(f.filename))
    #         return render_template('admin/upload.html')
    #     finally:
    #         return redirect(url_for('admin.product_manage'))




# import psycopg2
# conn = psycopg2.connect("dbname=psycopg_test user=postgres password=reza80reza80")

# cur = conn.cursor()
# cur.execute("SELECT id, name, address, salary  from COMPANY")
# rows = cur.fetchall()
# print(rows)
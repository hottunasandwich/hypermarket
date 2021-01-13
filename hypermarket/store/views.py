from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app, session, g
from werkzeug.utils import secure_filename
from hypermarket.admin.forms import LoginForm
from hypermarket.login_required import login_required
from persiantools.jdatetime import JalaliDate
from unidecode import unidecode
import os
import json
from ..db import get_db
import psycopg2
import psycopg2.extras
import json
from datetime import datetime

store_bp = Blueprint(
    'store', __name__, template_folder='templates', static_folder='static')


@store_bp.route('/')
def home():
    # cursor.execute("SELECT * FROM category WHERE customer_id = %s", (customer_id,))
    # g.customer = cursor.fetchone()
    # print(g.customer)
    db = get_db()
    with db:

        with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(
                "select category_name,category_id from category where parent_group=0")
            categories = [dict(row) for row in cursor.fetchall()]
            # print(categories)
            total_product = {}

            for x in categories:
                cursor.execute(f"""select DISTINCT ON (product_name) product_name, product_ware.product_id, price, category_name, image_link from product
                                    join category on product.category_id=category.category_id
                                    join product_ware on product.id=product_ware.product_id
                                    where parent_group={x['category_id']} and product_ware.number>0
                                    order by  product_name, product_date desc, price asc
                                    limit 4;""")
                each_product = [dict(row) for row in cursor.fetchall()]
                total_product[x['category_name']] = each_product

            # print(total_product.keys())

    return render_template('store/home.html', total_product=total_product, whole_cart=session['cart'])


# print(url_for('login', next='/'))
@store_bp.route('/category/?name=<category_name>')
def category_selector(category_name):
    db = get_db()
    with db:
        with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(
                f"select category_id from category where category_name like'%{category_name}%';")
            category_num = cursor.fetchone()['category_id']

            cursor.execute(
                f"""select parent_group from category where category_id={category_num}""")
            parent = cursor.fetchone()['parent_group']

            if not parent:

                cursor.execute(f"""select DISTINCT ON (product_name) product_name, product_ware.product_id, price, category_name, image_link from product
                                    join category on product.category_id=category.category_id
                                    join product_ware on product.id=product_ware.product_id
                                    where parent_group={category_num}
                                    order by  product_name, product_date desc, price asc;""")
            else:
                cursor.execute(f"""select DISTINCT ON (product_name) product_name, product_ware.product_id, price, category_name, image_link, category.category_id from product
                                    join category on product.category_id=category.category_id
                                    join product_ware on product.id=product_ware.product_id
									where category.category_id={category_num}
                                    order by  product_name, product_date desc, price asc;""")

            each_product = [dict(row) for row in cursor.fetchall()]

            with open('hypermarket/store/categories.json') as f:
                data = json.load(f)

    return render_template('store/category.html', each_product=each_product, category_name=category_name, data=data, whole_cart=session['cart'])


@store_bp.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_selector(product_id):
    db = get_db()
    with db:
        with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(f"""select product_name, image_link, price, description, category_name, category.category_id, product_ware.ware_id from product 
                                join product_ware on product.id=product_ware.product_id
                                join category on product.category_id=category.category_id
                                where product.id={product_id} and number>0
                                order by price asc
                                limit 1;""")
            product = cursor.fetchone()
            cursor.execute(f"""select sum(number) from product 
                                join product_ware on product.id=product_ware.product_id
                                where product.id={product_id} and number>0 and product_ware.ware_id={product['ware_id']}
                                group by product_id;""")
            total = cursor.fetchone()
            cat_id = product['category_id']

            category_path = []

            while True:
                cursor.execute(
                    f"""select parent_group, category_name from category where category_id = {cat_id}""")
                _all = cursor.fetchone()
                cat_id, cat_name = _all['parent_group'], _all['category_name']
                category_path = [cat_name] + category_path
                if not cat_id:
                    break

    product_id = str(product_id)
    in_cart = None
    if product_id in session['cart']:
        in_cart = session['cart'][product_id][0]

    if request.method == 'POST':
        try:
            client_order_count = int(request.form['count'])
            if client_order_count > total['sum'] or client_order_count < 1:
                raise Exception

            session['cart'][product_id] = (
                client_order_count, product['ware_id'])
            flash('به سبد خرید شما اضافه شد', 'success')

        except ValueError:
            flash('تعداد کالا ها قابل قبول نیست', 'danger')

        except Exception:
            flash('مقدار درخواستی شما قابل دسترس نیست', 'danger')

        return redirect(url_for('store.product_selector', product_id=product_id))

    return render_template('store/product.html', product=product, total=total, category_path=category_path, product_id=product_id, in_cart=in_cart, whole_cart=session['cart'])


@store_bp.route('/cart')
def cart_creation():
    products = []
    db = get_db()
    with db:
        with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            for product_id, count_ware_id in session['cart'].items():
                cursor.execute(f"""select product_name, product.id, image_link, price from product 
                                    join product_ware on product.id=product_ware.product_id
                                    join category on product.category_id=category.category_id
                                    where product.id={product_id} and number>0 and product_ware.ware_id={count_ware_id[1]}""")
                _ = cursor.fetchone()
                _['count'] = count_ware_id[0]
                products.append(_)

    if session['cart']:
        session['approved_cart'] = True

    return render_template('store/cart.html', products=products, whole_cart=session['cart'])


@store_bp.route('/cart/approve', methods=['POST', 'GET'])
def cart_approve_function():
    total_price = 0
    if session.get('approved_cart') and session['cart']:
        if request.method == 'POST':
            db = get_db()
            with db:
                with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                    details = []
                    for product_id, value in session['cart'].items():
                        cursor.execute(
                            f"""select price, product_ware.id, number, product_name, image_link from product_ware
                            join product on product.id=product_ware.product_id
                            where product_id={int(product_id)} and ware_id={value[1]}
                            """)
                        _ = cursor.fetchone()
                        total_price = total_price + (int(value[0]) * int(_['price']))
                        details.append((_['id'], _['number'] - int(value[0]), _['product_name'], _['image_link'], int(value[0])))

                    jalali_time = [int(i) for i in unidecode(request.form['date']).split('/')]
                    cursor.execute("""INSERT INTO orders (username,phone_number,address,delivery_time,order_time,total_cost)
                    VALUES (%s,%s,%s,%s,%s,%s) RETURNING order_id;""",
                                   (request.form['first_name'] + " " + request.form['last_name'], request.form['phone'], request.form['address'], JalaliDate(jalali_time[0], jalali_time[1], jalali_time[2]).to_gregorian(), datetime.now(), total_price))
                    order_id = cursor.fetchone()['order_id']

                    for index, o in enumerate(session['cart'].items(), start=0):
                        cursor.execute("""INSERT INTO cart (product_ware_id, order_id, count)
                        VALUES (%s,%s,%s)""",
                                    (details[index][0], order_id, o[1][0]))
                    
                        cursor.execute("""UPDATE product_ware SET number=%s WHERE id=%s""", (details[index][1], details[index][0]))

                    session.pop('cart', None)
                    session.pop('cart_approved', None)
                    return render_template('store/order_success.html', cart_detail=details, client_info=request.form, total_price=total_price, delivery_date=request.form['date'])

        return render_template('store/cart_approve.html', whole_cart=session['cart'])

    return 'Not approved for checkout'
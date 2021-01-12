from flask import Blueprint, jsonify, request, json, flash
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from persiantools.jdatetime import JalaliDate
from ..db import get_db
import psycopg2.extras
import os
import pandas as pd

api_bp = Blueprint('api', __name__)


@api_bp.route('/product/list')
def product_list():
    db = get_db()
    with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select id, product_name, category, image_link from product order by id")
        data = cur.fetchall()
    return jsonify(data)


@api_bp.route('/product/get_category')
def get_category():
    db = get_db()

    def find_sub_groups(parent_id):
        with db.cursor() as curs:
            curs.execute("select * from category where parent_group=%s", (parent_id,))
            return curs.fetchall()

    # ===================> for category with json format <===================
    # with open("hypermarket/store/categories.json", encoding='utf-8') as file:
    #     data = json.load(file)
    #     global category_list
    #     category_list = []
    #     for i in data:
    #         y = str(i['name'])
    #         for j in i['subcategories']:
    #             category_list.append(y + ' / ' + j['name'])
    with db.cursor() as cur:
        parent_cat = find_sub_groups(0)
        y = dict()
        for i in parent_cat:
            x = [f'{i[1]} / ', 0]
            sub_group2 = find_sub_groups(i[0])
            if sub_group2:
                for j in sub_group2:
                    x[0] = f"{i[1]} / {j[1]}"
                    x[1] = j[0]
                    sub_group3 = find_sub_groups(j[0])
                    if sub_group3:
                        for k in sub_group3:
                            x[0] = f"{i[1]} / {j[1]} /{k[1]}"
                            x[1] = k[0]
                            y[x[1]] = x[0]
                    else:
                        y[x[1]] = x[0]
            else:
                y[x[1]] = x[0]

    return jsonify(y)


@api_bp.route('/product/add_one', methods=["POST"])
def product_add_one():
    if request.method == "POST":
        db = get_db()
        category, category_id = request.form["cat-add"].split("|")
        try:
            f = request.files["img-add"]
            dir_path = os.path.join(r"static\uploads\images", secure_filename(f.filename))
            file_path = os.path.join(os.path.dirname(__file__).replace('api', 'admin'), dir_path)
            f.save(file_path)
            with db.cursor() as cur:
                cur.execute("insert into product(product_name,image_link,category_id,category) values(%s,%s,%s,%s);",
                            (request.form["pro-add"], dir_path, category_id, category,))
                db.commit()
        except FileNotFoundError:
            with db.cursor() as cur:
                cur.execute("insert into product(product_name,category_id,category) values(%s,%s,%s);",
                            (request.form["pro-add"], category_id, category,))
                db.commit()
    return "OK"


@api_bp.route('/product/add_file', methods=['POST'])
def product_add_file():
    if request.method == 'POST':
        f = request.files["fileUpload"]
        try:
            file_path = r"hypermarket\admin\static\uploads\files\\" + secure_filename(f.filename)
            if os.path.splitext(file_path)[-1] in [".xls", ".xlsx", ".csv"]:
                f.save(file_path)
                read_file = pd.read_excel(file_path)
                read_file.to_csv(file_path, index=None, header=True)
            else:
                raise NotImplementedError()
        except:
            abort(500, description="File Converting Was Not Successful!")
        with open(file_path, encoding='UTF-8') as cvs_file:
            for i in cvs_file.readlines():
                data = i.split(",")
                db = get_db()
                with db.cursor() as cur:
                    try:
                        cur.execute(
                            "insert into product(product_name,image_link,description,category) values(%s,%s,%s,%s);",
                            (data[0], data[1], data[2], data[3],))
                    except:
                        abort(500, description="Operation Was Not Successful!")
                        db.rollback()
            db.commit()
    return "OK"


@api_bp.route('/product/edit', methods=['POST'])
def product_edit():
    if request.method == 'POST':
        product_id, name, category = request.form["id"], request.form["name"], request.form["category"]
        db = get_db()
        with db.cursor() as cur:
            cur.execute("update product set product_name = %s, category = %s where id=%s;",
                        (name, category, product_id,))
            db.commit()
    else:
        return 'NOT OK'
    return 'OK'


@api_bp.route('/product/delete/<int:product_id>')
def product_delete(product_id):
    db = get_db()
    with db.cursor() as cur:
        cur.execute("delete from product_ware where product_id= %s ;", (product_id,))
        db.commit()
        cur.execute("delete from product where id= %s", (product_id,))
        db.commit()
    return "OK"


@api_bp.route('/warehouse/list')
def warehouse_list():
    db = get_db()
    with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select warehouse_name, warehouse_id from warehouse order by warehouse_id;")
        data = cur.fetchall()
    return jsonify(data)


@api_bp.route('/warehouse/add', methods=['POST'])
def warehouse_add():
    if request.method == 'POST' and request.form["nameWH"]:
        name = request.form["nameWH"]
        db = get_db()
        with db.cursor() as cur:
            cur.execute("insert into warehouse(warehouse_name) values(%s);", (name,))
            db.commit()
    else:
        return 'NOT OK'
    return 'OK'


@api_bp.route('/warehouse/edit', methods=['POST'])
def warehouse_edit():
    if request.method == 'POST' and request.form["nameModify"]:
        ware_id, modified_name = request.form["rowId"], request.form["nameModify"]
        db = get_db()
        with db.cursor() as cur:
            cur.execute("update warehouse set warehouse_name = %s where warehouse_id=%s;", (modified_name, ware_id,))
            db.commit()
    else:
        return 'NOT OK'
    return 'OK'


@api_bp.route('/warehouse/delete/<int:warehouse_id>')
def warehouse_delete(warehouse_id):
    db = get_db()
    with db.cursor() as cur:
        cur.execute("delete from product_ware where ware_id= %s;", (warehouse_id,))
        db.commit()
        cur.execute("delete from warehouse where warehouse_id= %s", (warehouse_id,))
        db.commit()
    return "OK"


@api_bp.route('/inventory_price/list')
def inventory_price_list():
    db = get_db()
    with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select pw.product_id, pw.ware_id, wh.warehouse_name, pr.product_name, pw.price, pw.number "
                    "from product_ware as pw "
                    "join product as pr on pw.product_id = pr.id "
                    "join warehouse as wh on pw.ware_id = wh.warehouse_id "
                    "order by pw.id;")
        data = cur.fetchall()
        for i in data:
            i['price'] = '{:,d}'.format(int(i['price']))

    return jsonify(data)


@api_bp.route('/inventory_price/detail')
def inventory_price_detail():
    db = get_db()
    with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select id, product_name from product")
        pro = cur.fetchall()
        cur.execute("select warehouse_id, warehouse_name from warehouse")
        ware = cur.fetchall()

    return jsonify([pro, ware])


@api_bp.route('/inventory_price/add', methods=['POST'])
def inventory_price_add():
    if request.method == 'POST':
        product_id, ware_id, number, price = request.form["pro_id"], request.form["ware_id"], \
                                             request.form["number"], request.form["price"]
        db = get_db()
        with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("insert into product_ware(product_id,ware_id, number, price) values(%s,%s,%s,%s);",
                        (product_id, ware_id, number, price))
            db.commit()
            return "OK"
    return "NOT OK"


@api_bp.route('/inventory_price/edit', methods=['POST'])
def inventory_price_edit():
    if request.method == 'POST':
        pro_id, price, number, ware_id = request.form["product_id"], request.form["new_price"], \
                                         request.form["new-inventory"], request.form["ware_id"]
        db = get_db()
        with db.cursor() as cur:
            cur.execute("update product_ware set "
                        "price = %s , number = %s where product_id= %s and ware_id = %s;",
                        (price, number, pro_id, ware_id,))
            db.commit()
        return "OK"
    return "NOT OK"


@api_bp.route('/inventory_price/delete', methods=['POST'])
def inventory_price_delete():
    pro_id, ware_id = request.form['allId'].split(".")
    print(pro_id)
    db = get_db()
    with db.cursor() as cur:
        try:
            cur.execute("delete from product_ware where product_id= %s and ware_id =%s;", (pro_id, ware_id,))
            # db.commit()
        except:
            abort(500, description="product was ordered , Unable to delete ordered products!")
    return "OK"


@api_bp.route('/order/list')
def order_list():
    db = get_db()
    with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select order_id,username, total_cost, order_time from orders order by order_id")
        data = cur.fetchall()
        for i in data:
            i['order_time'] = JalaliDate(i['order_time']).isoformat().replace('-', '/')
            i['total_cost'] = '{:,d}'.format(int(i['total_cost']))
        return jsonify(data)


@api_bp.route('/order/<int:order_id>')
def order_details(order_id):
    db = get_db()
    with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select * from orders where order_id= %s;", (order_id,))
        data = cur.fetchall()
        for i in data:
            i['order_time'], i['delivery_time'] = JalaliDate(i['order_time']).isoformat().replace('-', '/'), \
                                                  JalaliDate(i['order_time']).isoformat().replace('-', '/')

    return jsonify(data)

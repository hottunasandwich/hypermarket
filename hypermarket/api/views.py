from flask import Blueprint, jsonify, request
from persiantools.jdatetime import JalaliDate
from ..db import get_db
import psycopg2.extras

api_bp = Blueprint('api', __name__)


@api_bp.route('/product/list')
def product_list():
    db = get_db()
    with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select id, product_name, category_id, image_link from product")
        data = cur.fetchall()
    return jsonify(data)


@api_bp.route('/product/<int:product_id>')
def product_details(product_id):
    return ""


@api_bp.route('/product/add', methods=['POST'])
def product_add():
    pass


@api_bp.route('/product/edit', methods=['POST'])
def product_edit():
    pass


@api_bp.route('/product/delete/<int:product_id>')
def product_delete(product_id):
    db = get_db()
    with db.cursor() as cur:
        cur.execute("delete from product_ware where product_id= %s;", (product_id,))
        # db.commit()
        cur.execute("delete from product where id= %s", (product_id,))
        # db.commit()
    return "OK"


@api_bp.route('/product/upload')
def product_upload():
    pass


@api_bp.route('/warehouse/list')
def warehouse_list():
    db = get_db()
    with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select warehouse_name, warehouse_id from warehouse;")
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
                    "join warehouse as wh on pw.ware_id = wh.warehouse_id;")
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


@api_bp.route('/inventory_price/delete/<int:product_id>')
def inventory_price_delete(product_id):
    db = get_db()
    with db.cursor() as cur:
        cur.execute("delete from product_ware where product_id= %s;", (product_id,))
        db.commit()
    return "OK"


@api_bp.route('/order/list')
def order_list():
    db = get_db()
    with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select order_id,username, total_cost, order_time from orders;")
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

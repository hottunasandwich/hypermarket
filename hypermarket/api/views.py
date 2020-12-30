from flask import Blueprint, json, jsonify, request, flash
from persiantools.jdatetime import JalaliDate
from ..db import get_db
import psycopg2.extras

api_bp = Blueprint('api', __name__)


@api_bp.route('/product/list')
def product_list():
    pass


@api_bp.route('/product/<int:product_id>')
def product_details(product_id):
    pass


@api_bp.route('/product/add', methods=['POST'])
def product_add():
    pass


@api_bp.route('/product/edit', methods=['POST'])
def product_edit():
    pass


@api_bp.route('/product/delete/<int:product_id>')
def product_delete(product_id):
    pass


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
        print(ware_id, modified_name)
        db = get_db()
        with db.cursor() as cur:
            cur.execute("update warehouse set warehouse_name = %s where warehouse_id=%s;", (modified_name, ware_id,))
            db.commit()
            print('OK')
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


@api_bp.route('/quantity/list')
def quantity_list():
    pass


@api_bp.route('/quantity/add', methods=['POST'])
def quantity_add():
    pass


@api_bp.route('/quantity/edit', methods=['POST'])
def quantity_edit():
    pass


@api_bp.route('/quantity/delete/<int:quantity_id>')
def quantity_delete(quantity_id):
    pass


@api_bp.route('/order/list')
def order_list():
    db = get_db()
    with db.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("select order_id,username, total_cost, order_time from orders;")
        data = cur.fetchall()
        print(data)
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
        print(data)
        for i in data:
            i['order_time'], i['delivery_time'] = JalaliDate(i['order_time']).isoformat().replace('-', '/'), \
                                                  JalaliDate(i['order_time']).isoformat().replace('-', '/')

    return jsonify(data)

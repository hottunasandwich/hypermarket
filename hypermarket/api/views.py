from flask import Blueprint

api_bp = Blueprint(
    'api',
    __name__
)

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
    pass

@api_bp.route('/warehouse/add', methods=['POST'])
def warehouse_add():
    pass

@api_bp.route('/warehouse/edit', methods=['POST'])
def warehouse_edit():
    pass

@api_bp.route('/warehouse/delete/<int:warehouse_id>')
def warehouse_delete(warehouse_id):
    pass

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
    pass

@api_bp.route('/order/<int:order_id>')
def order_details(order_id):
    pass
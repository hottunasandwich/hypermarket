from flask import Flask, session
import os


def set_cart():
    if 'cart' not in session:
        session['cart'] = {}
    # print(f'cart value set to: {session["cart"]}')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.before_request(set_cart)
    app.config.from_pyfile('config.py', silent=True)
    app.config.from_mapping(
        DB_NAME="hyper_sabzi",
        DB_USER="postgres",
        DB_PASS="eshaq79"
    )
    if test_config is not None:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register blueprints here
    from hypermarket.admin.views import admin_bp
    
    
    from hypermarket.store.views import store_bp
    ####### line 20 ro eslah kardam

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(store_bp, url_prefix='/')
    
    
    
    
    
    
    from hypermarket.api.views import api_bp

    app.register_blueprint(api_bp, url_prefix='/api')

    return app

#########################????????????????????????????????????????????
    # from flaskr import db

    # db.init_app(app)

    # from flaskr import auth, blog
    # app.register_blueprint(auth.bp)
    # app.register_blueprint(blog.bp)

    # # make url_for('index') == url_for('blog.index')
    # # in another app, you might define a separate main index here with
    # # app.route, while giving the blog blueprint a url_prefix, but for
    # # the tutorial the blog will be the main index
    # app.add_url_rule("/", endpoint="index")


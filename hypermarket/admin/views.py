from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app, session
from hypermarket.admin.forms import LoginForm
from hypermarket.login_required import login_required

admin_bp = Blueprint(
    'admin',
    __name__,
    template_folder='templates',
    static_folder='static'
)


def check_authentication(username, password):
    # TODO: add database of admins
    return {username: password} in current_app.config.get('ADMIN')

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

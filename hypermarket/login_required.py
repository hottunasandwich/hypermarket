from flask import session, url_for, redirect
from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return func(*args, **kwargs)

        else:
            return redirect(url_for('admin.login'))

    return wrapper

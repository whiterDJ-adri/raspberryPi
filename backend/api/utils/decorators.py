from flask import session, redirect, url_for
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login.show_page_login"))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login.show_page_login"))

        if not session.get("isAdmin"):
            return redirect(url_for("dashboard.dashboard"))

        return f(*args, **kwargs)

    return decorated_function

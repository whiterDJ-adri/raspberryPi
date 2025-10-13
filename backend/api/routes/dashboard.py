from flask import Blueprint, render_template, redirect, url_for, session

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():
    if "email" not in session:
        return redirect(url_for("login.show_page_login"))

    if "isAdmin" in session and session["isAdmin"]:
        return redirect(url_for("dashboard.admin_dashboard"))

    return render_template("dashboard_user.html")


@dashboard_bp.route("/admin")
def admin_dashboard():
    if "email" not in session:
        return redirect(url_for("login.show_page_login"))
    
    if "isAdmin" in session and session["isAdmin"]:
        return render_template("dashboard_admin.html")
    
    return redirect(url_for("dashboard.dashboard"))

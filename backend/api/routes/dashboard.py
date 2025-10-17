from flask import Blueprint, render_template, redirect, url_for, session
from utils.decorators import login_required, admin_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
def dashboard():
    if "isAdmin" in session and session["isAdmin"]:
        return redirect(url_for("dashboard.admin_dashboard"))

    return render_template("dashboard_user.html")


@dashboard_bp.route("/admin")
@admin_required
def admin_dashboard():
    return render_template("dashboard_admin.html")


@dashboard_bp.route("/admin/manage-users")
@admin_required
def admin_panel():
    return render_template("components/user_management.html")

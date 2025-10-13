from flask import (
    Blueprint,
    request,
    jsonify,
    current_app,
    render_template,
    session,
    redirect,
    url_for,
)
from schemes import user_schema
from controllers.login_bd import LoginController

login_bp = Blueprint("login", __name__)


def get_login_controller():
    return LoginController(current_app.mongo)


@login_bp.route("/", methods=["GET"])
def show_page_login():
    if "email" in session:
        return redirect(url_for("dashboard.dashboard"))
    
    return render_template("login.html")


@login_bp.route("/login", methods=["POST"])
def login():
    data = request.json 
    email = data.get("email")
    password = data.get("password")

    controller = get_login_controller()
    user = controller.get_user(email)

    if user is None:
        return jsonify({"message": "Invalid credentials"}), 401

    if user.get("password") != password:
        return jsonify({"message": "Invalid credentials"}), 401

    session["email"] = email
    session["isAdmin"] = user.get("isAdmin", False)

    return redirect(url_for("dashboard.dashboard"))


@login_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    validated_data = user_schema.load(data)

    data_email = validated_data.get("email")

    login_controller = get_login_controller()
    existing_user = login_controller.get_user(data_email)

    if existing_user is not None:
        return jsonify({"message": "User already exists"}), 400

    login_controller.create_user(validated_data)

    return jsonify({"message": "User created succesfully"}), 201


@login_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login.show_page_login"))

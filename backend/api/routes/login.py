from flask import Blueprint, request, jsonify, current_app, render_template
from schemes import user_schema
from controllers.login_bd import LoginController

login_bp = Blueprint("login", __name__)


def get_login_controller():
    return LoginController(current_app.mongo)


@login_bp.route("/login/login", methods=["POST"])
def login():
    data = request.json
    validated_data = user_schema.load(data)
    data_email = validated_data.get("email")
    data_password = validated_data.get("password")

    login_controller = get_login_controller()
    data_bd = login_controller.get_user(data_email)

    if data_bd is None:
        return jsonify({"message": "User not found"}), 404

    if data_bd.get("password") != data_password:
        return jsonify({"message": "Invalid password"}), 401

    return render_template("index.html"), 200

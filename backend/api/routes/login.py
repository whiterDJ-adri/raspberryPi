from flask import Blueprint, request, jsonify, current_app, render_template
from schemes import user_schema
from controllers.login_bd import LoginController

login_bp = Blueprint("login", __name__)
signup_bp = Blueprint("signup", __name__)


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


@signup_bp.route("/signup/signup", methods=["POST"])
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
    
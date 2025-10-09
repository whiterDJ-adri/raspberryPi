from flask import Blueprint, request, jsonify
# from controllers.login_controller import LoginController

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    return jsonify({"message": "Login successful"}), 200
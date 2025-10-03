from flask import Blueprint, jsonify, current_app, request
from schemes import record_camera_schema
from controllers.record_camera import RecordCameraController

record_cam_bp = Blueprint('record_camera', __name__)

def get_controller():
    return RecordCameraController(current_app.mongo)

@record_cam_bp.route('/', methods=['GET'])
def get_photos():
    controller = get_controller()
    records = controller.get_one_route()
    return jsonify(records), 200

@record_cam_bp.route('/', methods=['POST'])
def add_user():
    data = record_camera_schema.load(request.json)
    controller = get_controller()
    record = controller.add_photo(data)
    return jsonify(record_camera_schema.dump(record)), 201


import os
from flask import Blueprint, jsonify, current_app, request
from schemes import record_camera_schema
from controllers.record_camera_bd import RecordCameraController

# Hace referencia al blueprint que se creo, le pasa el nombre para identificar al blueprint y donde se hace referencia
record_cam_bp = Blueprint("record_camera", __name__)


# Funciones para obtener los controladores que vamos a usar
def get_db_controller():
    return RecordCameraController(current_app.mongo)


def get_record_controller():
    return RecordCameraController(current_app.mongo)


@record_cam_bp.route("/", methods=["GET"])
def obtener_foto():
    rc = get_record_controller()
    response = rc.get_all_photos()
    return jsonify(response), response[1]


@record_cam_bp.route("/", methods=["POST"])
def add_foto():
    data = request.form.to_dict()

    data_db = {
        "filename": data.get("filename"),
        "date": data.get("date"),
        "file_path": os.path.join("media/screenshots", data.get("filename")),
    }

    data_file = request.files["file"]
    data_file.save(f"{data_db['file_path']}")

    validated_data = record_camera_schema.load(data_db)
    db = get_db_controller()
    result = db.add_photo(validated_data)
    return jsonify(result), result[1]


@record_cam_bp.route("/<photo_id>", methods=["GET"])
def obtener_una_foto(photo_id):
    db = get_db_controller()
    response = db.get_one_photo()
    return jsonify(response), response[1]


@record_cam_bp.route("/<photo_id>", methods=["DELETE"])
def borrar_foto(photo_id):
    db = get_db_controller()
    result = db.delete_photo(photo_id)
    return jsonify(result), result[1]


# @record_cam_bp.route('/', methods=['POST'])
# def hacer_una_foto():
#     # Se llama al controlador de la camara, se usa el metodo hacer_foto y el resultado que devuelve se guarda en data
#     # Se calida los datos, es decir se mria que coincida con el schema para poder insertar los datos correctos en la bd
#     # Después se llama a l controlador de la bd, y se usa el metodo add_photo para guardar los datos
#     camera = get_camera_controller()
#     data = camera.hacer_foto()
#     validated_data = record_camera_schema.load(data)
#     db = get_db_controller()
#     result = db.add_photo(validated_data)
#     # Devuelve o que da el metodo add_photo
#     return jsonify(result), result[1]

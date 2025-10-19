import os
from flask import (
    Blueprint,
    jsonify,
    current_app,
    request,
    send_from_directory,
    Response,
)
from schemes import record_camera_schema
from controllers.record_camera_bd import RecordCameraController
import services.missatge_discord as missatge_discord
import services.video as video

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

    # Obtener los args y si tiene el date se llama a la funcion get_photos_by_date en el controller db sino se obtienen todas las fotos
    date_filter = request.args.get("date")

    if date_filter:
        print(f"Filtrando por fecha: {date_filter}")
        response = rc.get_photos_by_date(date_filter)
    else:
        print("Obteniendo todas las fotos")
        response = rc.get_all_photos()

    print("Response: ", response)
    return jsonify(response), 200


@record_cam_bp.route("/", methods=["POST"])
def add_foto():
    data = request.form.to_dict()

    data_db = {
        "filename": data.get("filename"),
        "date": data.get("date"),
        "file_path": f"{os.path.join('media/screenshots', data.get('filename'))}",
    }

    data_file = request.files["file"]
    data_file.save(f"{data_db['file_path']}")

    validated_data = record_camera_schema.load(data_db)

    missatge_discord.send_message(validated_data)

    db = get_db_controller()
    result = db.add_photo(validated_data)
    return jsonify(result), 201


@record_cam_bp.route("/<photo_id>", methods=["GET"])
def obtener_una_foto(photo_id):
    db = get_db_controller()
    response = db.get_one_photo()
    return jsonify(response), 200


@record_cam_bp.route("/<photo_id>", methods=["DELETE"])
def borrar_foto(photo_id):
    db = get_db_controller()
    result = db.delete_photo(photo_id)
    return jsonify(result), result[1]


@record_cam_bp.route("/screenshots/<path:filename>")
def media(filename):
    directory = os.path.join(current_app.root_path, "media/screenshots")

    return send_from_directory(directory, filename, as_attachment=False)


@record_cam_bp.route("/photos/removeAll", methods=["DELETE"])
def clean_photos():
    db = get_db_controller()
    result = db.remove_all_photos()
    return jsonify(result), result[1]


@record_cam_bp.route("/photos/removeByDate/<date>", methods=["DELETE"])
def remove_photos_by_date(date):
    try:
        db = get_db_controller()
        result = db.remove_photos_by_date(date)
        return jsonify(result), result[1]
    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500


@record_cam_bp.route('/video')
def real_streaming():
    # Devuelve todas las imagenes del make_video al navegador, con el mimetype, se le indica el tipo de archivo que va a estar recibiendo
    # multipart --> Múltiples archivos
    # x-mixed-replace --> Cada vz que se envie remplaza la anterior
    # boundary=frame --> Separador entre cada mensaje, en este caso es frame
    return Response(video.make_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


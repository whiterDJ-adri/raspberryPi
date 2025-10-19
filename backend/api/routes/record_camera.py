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


# FALTA: Control de errores en subida de archivos
# - Validar que el archivo subido sea una imagen válida
# - Verificar el tamaño del archivo para evitar ataques
# - Manejar errores al guardar el archivo en disco
# - Validar datos del formulario antes de procesar
@record_cam_bp.route("/", methods=["POST"])
def add_foto():
    try:
        # Verificar que se recibieron datos del formulario
        if not request.form:
            return jsonify({"error": "No se recibieron datos del formulario"}), 400

        data = request.form.to_dict()

        # Verificar que se subió un archivo
        if "file" not in request.files:
            return jsonify({"error": "No se encontró archivo en la petición"}), 400

        data_file = request.files["file"]

        # Verificar que el archivo tiene nombre
        if data_file.filename == "":
            return jsonify({"error": "No se seleccionó ningún archivo"}), 400

        # Verificar que es una imagen (extensión básica)
        allowed_extensions = {"png", "jpg", "jpeg", "gif"}
        if not (
            "." in data_file.filename
            and data_file.filename.rsplit(".", 1)[1].lower() in allowed_extensions
        ):
            return jsonify({"error": "Tipo de archivo no permitido"}), 400

        # Verificar campos requeridos del formulario
        filename = data.get("filename", "").strip()
        date = data.get("date", "").strip()

        if not filename or not date:
            return jsonify({"error": "Filename y date son requeridos"}), 400

        data_db = {
            "filename": filename,
            "date": date,
            "file_path": f"{os.path.join('media/screenshots', filename)}",
        }

        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(data_db["file_path"]), exist_ok=True)
            # Guardar archivo
            data_file.save(f"{data_db['file_path']}")
        except Exception as e:
            print(f"Error al guardar archivo: {e}")
            return jsonify({"error": "Error al guardar el archivo"}), 500

        try:
            validated_data = record_camera_schema.load(data_db)
        except Exception as e:
            # Si hay error en validación, eliminar archivo ya guardado
            try:
                os.remove(data_db["file_path"])
            except Exception:
                pass
            return jsonify({"error": f"Datos inválidos: {str(e)}"}), 400

        try:
            missatge_discord.send_message(validated_data)
        except Exception as e:
            print(f"Error al enviar mensaje a Discord: {e}")
            # No fallar la petición si Discord falla, solo logear

        try:
            db = get_db_controller()
            result = db.add_photo(validated_data)
            return jsonify(result), 201
        except Exception as e:
            # Si falla la BD, eliminar archivo guardado
            try:
                os.remove(data_db["file_path"])
            except Exception:
                pass
            print(f"Error al guardar en base de datos: {e}")
            return jsonify({"error": "Error al guardar en base de datos"}), 500

    except Exception as e:
        print(f"Error inesperado en add_foto: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


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


@record_cam_bp.route("/video")
def real_streaming():
    # Devuelve todas las imagenes del make_video al navegador, con el mimetype, se le indica el tipo de archivo que va a estar recibiendo
    # multipart --> Múltiples archivos
    # x-mixed-replace --> Cada vz que se envie remplaza la anterior
    # boundary=frame --> Separador entre cada mensaje, en este caso es frame
    return Response(
        video.make_video(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )

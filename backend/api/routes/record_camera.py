from flask import Blueprint, jsonify, current_app, request
from schemes import record_camera_schema
from controllers.record_camera_bd import RecordCameraController
from controllers.camera import CameraController

# Hace referencia al blueprint que se creo, le pasa el nombre para identificar al blueprint y donde se hace referencia
record_cam_bp = Blueprint('record_camera', __name__)

# Funciones para obtener los controladores que vamos a usar
def get_db_controller():
    return RecordCameraController(current_app.mongo)

def get_camera_controller():
    return CameraController()

@record_cam_bp.route('/', methods=['POST'])
def hacer_una_foto():
    # Se llama al controlador de la camara, se usa el metodo hacer_foto y el resultado que devuelve se guarda en data
    camera = get_camera_controller()
    data = camera.hacer_foto()
    
    # Se calida los datos, es decir se mria que coincida con el schema para poder insertar los datos correctos en la bd
    validated_data = record_camera_schema.load(data)
    
    # Después se llama a l controlador de la bd, y se usa el metodo add_photo para guardar los datos
    db = get_db_controller()
    result = db.add_photo(validated_data)
    
    # Devuelve o que da el metodo add_photo
    return jsonify(result), 201

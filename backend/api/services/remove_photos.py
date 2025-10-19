import os
from flask import current_app
from controllers.record_camera_bd import RecordCameraController

current_dir = os.path.dirname(os.path.abspath(__file__))
photos_dir = os.path.join(current_dir, "..", "media", "screenshots")
photos_dir = os.path.abspath(photos_dir)

if not os.path.exists(photos_dir):
    os.makedirs(photos_dir)
    print(f"Directorio creado: {photos_dir}")

list_photos = os.listdir(photos_dir)


def get_record_controller():
    return RecordCameraController(current_app.mongo)


def detect_photos_exists():
    db = get_record_controller()
    photos_in_db = set()

    for photo in db.get_all_photos():
        photos_in_db.add(photo["filename"])

    for filename in list_photos:
        if filename not in photos_in_db:
            file_path = os.path.join(photos_dir, filename)
            try:
                os.remove(file_path)
                print(f"Imagen borrada: {filename}")
            except OSError as e:
                print(f"Error al borrar la imagen {filename}: {e}")

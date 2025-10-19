import os
from flask import current_app
from controllers.record_camera_bd import RecordCameraController

current_dir = os.path.dirname(os.path.abspath(__file__))
photos_dir = os.path.join(current_dir, "..", "media", "screenshots")
photos_dir = os.path.abspath(photos_dir)

if not os.path.exists(photos_dir):
    try:
        os.makedirs(photos_dir)
        print(f"Directorio creado: {photos_dir}")
    except OSError as e:
        print(f"Error al crear directorio {photos_dir}: {e}")

# FALTA: Control de errores al listar archivos
# - Manejar errores si el directorio no existe o no es accesible
try:
    list_photos = os.listdir(photos_dir)
except OSError as e:
    print(f"Error al listar fotos en {photos_dir}: {e}")
    list_photos = []


def get_record_controller():
    return RecordCameraController(current_app.mongo)


# FALTA: Control de errores más robusto
# - Manejar errores de base de datos al obtener fotos
# - Verificar permisos de escritura antes de eliminar archivos
# - Logs más detallados para debugging
def detect_photos_exists():
    try:
        # Verificar que el directorio existe y es accesible
        if not os.path.exists(photos_dir):
            print(f"Directorio de fotos no existe: {photos_dir}")
            return

        if not os.access(photos_dir, os.R_OK):
            print(f"Sin permisos de lectura en directorio: {photos_dir}")
            return

        db = get_record_controller()
        photos_in_db = set()

        try:
            # Obtener fotos de la base de datos
            db_photos = db.get_all_photos()

            # Verificar si hay error en la respuesta de la BD
            if isinstance(db_photos, tuple):  # Error response
                print(f"Error al obtener fotos de BD: {db_photos}")
                return

            for photo in db_photos:
                if "filename" in photo:
                    photos_in_db.add(photo["filename"])

        except Exception as e:
            print(f"Error al consultar base de datos: {e}")
            return

        # Obtener lista actualizada de archivos
        try:
            current_files = os.listdir(photos_dir)
        except OSError as e:
            print(f"Error al listar archivos actuales: {e}")
            return

        # Verificar permisos de escritura
        if not os.access(photos_dir, os.W_OK):
            print(f"Sin permisos de escritura en directorio: {photos_dir}")
            return

        deleted_count = 0
        for filename in current_files:
            if filename not in photos_in_db:
                file_path = os.path.join(photos_dir, filename)
                try:
                    # Verificar que es un archivo regular antes de eliminar
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Imagen borrada: {filename}")
                        deleted_count += 1
                    else:
                        print(f"Saltando {filename}: no es un archivo regular")
                except OSError as e:
                    print(f"Error al borrar la imagen {filename}: {e}")
                except Exception as e:
                    print(f"Error inesperado al borrar {filename}: {e}")

        if deleted_count > 0:
            print(f"Total de archivos eliminados: {deleted_count}")
        else:
            print("No se encontraron archivos para eliminar")

    except Exception as e:
        print(f"Error inesperado en detect_photos_exists: {e}")

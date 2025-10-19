from bson import ObjectId
from pymongo.errors import PyMongoError, ConnectionFailure
from datetime import datetime


class RecordCameraController:
    def __init__(self, mongo):
        self.collection = mongo.db["record_camera"]

    def get_one_photo(self, photo_id):
        photo = self.collection.find({"_id": ObjectId(photo_id)})
        return photo

    def get_all_photos(self):
        try:
            photos = self.collection.find({}, {"_id": 0})
            return photos

        except ConnectionFailure:
            return {"error": "Database connection failed"}, 503
        except PyMongoError as e:
            return {"error": f"Database error: {str(e)}"}, 500
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500

    def add_photo(self, data):
        self.collection.insert_one(data)
        return {"msg": "Photo record created"}

    def delete_photo(self, photo_id):
        result = self.collection.delete_one({"_id": ObjectId(photo_id)})
        if result.deleted_count == 1:
            return {"msg": "Photo record deleted"}, 200
        else:
            return {"msg": "Photo record not found"}, 404

    def get_photos_by_date(self, date_str):
        try:
            # Convertir la fecha del formato YYYY-MM-DD a YYYYMMDD que es como esta en la  BD
            # Si viene con guiones, los quitamos
            if "-" in date_str:
                # Se pasa el string a objeto fecha
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                # Se le da el formato
                date_formatted = date_obj.strftime("%Y%m%d")
            else:
                date_formatted = date_str

            print(f"Buscando fotos con fecha: {date_formatted}")

            # Crear expresión regular para buscar fechas que comiencen con el patrón en este caso con año-mes-dia porque no nos intreresan las horas
            date_pattern = f"^{date_formatted}"

            # Buscar, se usa $regex que es una expresion de busqueda en mongo que  cuadno pones ^ te indica el comienzo es decir se buscan los dates que empiezen por el año-mes-dia obtenido desde js
            photos = list(
                self.collection.find({"date": {"$regex": date_pattern}}, {"_id": 0})
            )

            print(f"Fotos encontradas para {date_formatted}: {len(photos)}")
            return photos

        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500

    def remove_all_photos(self):
        try:
            self.collection.delete_many({})
            return {"msg": "All photos removed"}, 200
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500

    def remove_photos_by_date(self, date_str):
        try:
            # Convertir la fecha del formato YYYY-MM-DD a YYYYMMDD que es como esta en la BD
            if "-" in date_str:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                date_formatted = date_obj.strftime("%Y%m%d")
            else:
                date_formatted = date_str

            print(f"Eliminando fotos con fecha: {date_formatted}")

            # Crear expresión regular para buscar fechas que comiencen con el patrón
            date_pattern = f"^{date_formatted}"

            # Eliminar fotos que coincidan con el patrón de fecha
            result = self.collection.delete_many({"date": {"$regex": date_pattern}})

            print(f"Fotos eliminadas para {date_formatted}: {result.deleted_count}")

            if result.deleted_count > 0:
                return {
                    "msg": f"Se eliminaron {result.deleted_count} fotos del {date_str}"
                }, 200
            else:
                return {"msg": f"No se encontraron fotos para la fecha {date_str}"}, 404

        except Exception as e:
            return {"error": f"Error al eliminar fotos: {str(e)}"}, 500

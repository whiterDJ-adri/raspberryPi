from bson import ObjectId
from flask import Response
import os
from pymongo.errors import PyMongoError, ConnectionFailure, OperationFailure

"""
    PyMongoError:           Error base genérico
    ConnectionFailure:      Problemas de conexión
    OperationFailure:       Fallo en operaciones
"""


class RecordCameraController:
    def __init__(self, mongo):
        self.collection = mongo.db["record_camera"]

    def get_one_photo(self, photo_id):
        response = self.collection.find({"_id": ObjectId(photo_id)})
        return response, 200

    # def get_one_photo(self, photo_id):
    #     try:
    #         if not photo_id:
    #             return {"error": "Photo ID is required"}, 400

    #         obj_id = ObjectId(photo_id)

    #         response = self.collection.find_one({"_id": obj_id})

    #         if response is None:
    #             return {"error": "Photo record not found"}, 404

    #         response["_id"] = str(response["_id"])

    #         return response, 200

    #     except ConnectionFailure:
    #         return {"error": "Database connection failed"}, 503
    #     except PyMongoError as e:
    #         return {"error": f"Database error: {str(e)}"}, 500
    #     except Exception as e:
    #         return {"error": f"Unexpected error: {str(e)}"}, 500

    def get_all_photos(self):
        response = self.collection.find()
        return response, 200

    def add_photo(self, data):
        self.collection.insert_one(data)
        return {"msg": "Photo record created"}, 201

    def delete_photo(self, photo_id):
        result = self.collection.delete_one({"_id": ObjectId(photo_id)})
        if result.deleted_count == 1:
            return {"msg": "Photo record deleted"}, 200
        else:
            return {"msg": "Photo record not found"}, 404
    
    def get_image_file(self, photo_id):
        """Lee el archivo local de la foto y lo devuelve como imagen."""
        try:
            photo, status = self.get_one_photo(photo_id)
            if status != 200:
                return photo, status

            path = photo.get("file_path")
            if not path or not os.path.exists(path):
                return {"error": "Image file not found"}, 404

            with open(path, "rb") as f:
                image_data = f.read()

            return Response(image_data, mimetype="image/jpeg"), 200

        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500


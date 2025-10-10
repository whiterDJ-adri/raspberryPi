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
        photo = self.collection.find({"_id": ObjectId(photo_id)})
        return photo

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
        try:
            photos = self.collection.find({}, {"_id": 1})
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
    
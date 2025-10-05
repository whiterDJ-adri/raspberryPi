from bson import ObjectId
from datetime import datetime

class RecordCameraController:
    def __init__(self, mongo):
        self.collection = mongo.db["record_camera"]
    
    def get_one_photo(self, photo_id):
        record = self.collection.find({"_id": ObjectId(photo_id)})
        return record, 200
    
    def get_all_photos(self):
        records = self.collection.find()
        return records, 200
    
    def add_photo(self, data):
        self.collection.insert_one(data)
        return {"msg": "Photo record created"}, 201

    def delete_photo(self, photo_id):
        result = self.collection.delete_one({"_id": ObjectId(photo_id)})
        if result.deleted_count == 1:
            return {"msg": "Photo record deleted"}, 200
        else:
            return {"msg": "Photo record not found"}, 404
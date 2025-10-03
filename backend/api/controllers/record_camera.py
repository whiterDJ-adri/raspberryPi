from bson import ObjectId
from datetime import datetime

class RecordCameraController:
    def __init__(self, mongo):
        self.collection = mongo.db["record_camera"]
    
    def get_one_route(self):
        records = self.collection.find().limit(1)
        return records
    
    def add_photo(self, data):
        self.collection.insert_one(data)
        return {"msg": "Photo record created"}
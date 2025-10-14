

class LoginController:
    def __init__(self, mongo):
        self.collection = mongo.db["users"]
    
    def get_user(self, email):
        user = self.collection.find_one({"email": email})
        return user
    
    def create_user(self, user_data):
        self.collection.insert_one(user_data)
    
    def delete_user(self, email):
        self.collection.delete_one({"email": email})
    
    def get_all_users(self):
        return list(self.collection.find({}, {"_id": 0}))  
        
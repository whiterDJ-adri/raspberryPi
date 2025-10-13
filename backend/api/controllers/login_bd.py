

class LoginController:
    def __init__(self, mongo):
        self.collection = mongo.db["users"]
    
    def get_user(self, email):
        user = self.collection.find_one({"email": email})
        return user
    
    def create_user(self, user_data):
        self.collection.create_one(user_data)
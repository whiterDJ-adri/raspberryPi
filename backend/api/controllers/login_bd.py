

class LoginController:
    def __init__(self, mongo):
        self.collection = mongo.db["login"]
    
    def get_user(self, email):
        user = self.collection.find_one({"email": email})
        return user
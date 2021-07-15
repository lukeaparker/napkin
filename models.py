import bcrypt 

class Users():

    def __init__(self, db):
        self.users = db.users 
    
    def create_user(self, user):
        self.users.insert_one(user)
        user = self.users.find_one({'email': user['email']})

    
    def verify_credentials(self, user_credentials):
        user = self.users.find_one({'email': user_credentials['email']})
        if not user or not bcrypt.checkpw(user_credentials['password'], user['password']):
            return False 
        else:
            return user 
    
    def find_user(self, _id):
        user = self.users.find_one({'_id': _id})
        return user   
  







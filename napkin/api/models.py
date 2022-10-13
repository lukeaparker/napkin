import bcrypt 

class Users():

    def __init__(self, db):
        self.users = db.users 
    
    def create_user(self, user):
        self.users.insert_one(user)
        user = self.users.find_one({'email': user['email']})
        print(user)

    
    def verify_credentials(self, user_credentials):
        print('cred', user_credentials)
        user = self.users.find_one({'email': user_credentials['email']})
        print('user', user)
        if user and bcrypt.checkpw(user_credentials['password'], user['password']):
            return user 
        else:
            print('login failed')
            return False 
    
    def find_user(self, _id):
        user = self.users.find_one({'_id': _id})
        return user   
  







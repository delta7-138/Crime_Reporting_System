from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

#to allow flask_login to load user and grab the id
#once someone logged we will be able to show pages specific to their login
@login_manager.user_loader   # user_loader is builtin decorator in login manager
def load_user(user_id):
    return User.query.get(user_id) # to grab that id specific to the user



class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(64),unique = True,index =True) #email can take max 64 characters
    username = db.Column(db.String(64),unique = True,index =True)
    password_hash = db.Column(db.String(128))

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
       return check_password_hash(self.password_hash,password)

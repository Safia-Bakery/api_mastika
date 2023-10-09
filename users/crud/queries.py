from users.models.models import *



class UserService:
    def __init__(self, db) -> None:
        """User Service"""
        self.db = db
    def get_users(self):
        result = self.db.query(Users).all()
        return result
    def create_user(self,username,password):
        query = Users(username=username,password=password)
        self.db.add(query)
        self.db.commit()
        self.db.refresh(query)
        return query
    def get_user(self,username):
        result = self.db.query(Users).filter(Users.username==username).first()
        return result

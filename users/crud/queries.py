from users.models.models import *



class UserService:
    def __init__(self, db) -> None:
        """User Service"""
        self.db = db
    def get_users(self):
        result = self.db.query(Users).all()
        return result
    def create_user(self,username,password,phone_number):
        query = Users(username=username,password=password,phone_number=phone_number)
        self.db.add(query)
        self.db.commit()
        self.db.refresh(query)
        return query
    def get_user(self,username):
        result = self.db.query(Users).filter(Users.username==username).first()
        return result
    def get_user_withph(self,phone_number):
        result = self.db.query(Users).filter(Users.phone_number==phone_number).first()
        return result
    def get_or_create(self,phone_number):
        query = self.db.query(Users).filter(Users.phone_number==phone_number).first()
        if query:
            return query
        data = Users(phone_number=phone_number,is_client=1)
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data
    
        

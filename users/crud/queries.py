from users.models.models import *
from users.schemas.user_schema import UserUpdate
from users.utils.user_micro import *


class UserService:
    def __init__(self, db) -> None:
        """User Service"""
        self.db = db
    def get_users(self,id,is_client):
        result = self.db.query(Users)
        if id is not None:
            result = result.filter(Users.id==id)
        if is_client is not None:
            result = result.filter(Users.is_client ==is_client)
        
        
        return result.all()
    def create_user(self,username,password,phone_number,full_name,status,role_id):
        query = Users(username=username,password=password,phone_number=phone_number,full_name=full_name,status=status,role_id=role_id)
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
    
    def user_update(self,form_data:UserUpdate):
        query  = self.db.query(Users).filter(Users.id==form_data.id).first()
        if query:
            if form_data.username is not None:
                query.username = form_data.username
            if form_data.password is not None:
                query.password = hash_password(password=form_data.password)
            if form_data.phone_number is not None:
                query.phone_number = form_data.phone_number
            if form_data.full_name is not None:
                query.full_name=form_data.full_name
            if form_data.status is not None:
                query.status=form_data.status
            if form_data.role_id is not None:
                query.role_id = form_data.role_id
            self.db.commit()
            self.db.refresh(query)
            return query
        else:
            return query
    def set_null_permissions(self,id):
        self.db.query(Permissions).filter(Permissions.role_id==id).delete()
        self.db.commit()
        return True

    def def_add_permissions(self,per_obj):
        self.db.bulk_save_objects(per_obj)
        self.db.commit()
        return True
    def create_role(self,name):
        query  = Roles(name=name)
        self.db.add(query)
        self.db.commit()
        self.db.refresh(query)
        return query
    def get_roles(self,id):
        query = self.db.query(Roles)
        if id is not None:
            query = query.filter(Roles.id==id)
        return query.all()
    def role_update(self,name,role_id):
        query = self.db.query(Roles).filter(Roles.id==role_id).first()
        query.name=name
        self.db.commit()
        self.db.refresh(query)
        return query
    def get_pages(self,):
        query = self.db.query(Pages).all()
        return query
    def all_permissions(self):
        query = self.db.query(PageCrud).all()
        return query
    
        
    
    
    
        

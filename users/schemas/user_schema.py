from pydantic import BaseModel,validator
from typing import Optional,Dict
from datetime import datetime

class PageCrud(BaseModel):
    id:int
    name:str
    class Config:
        orm_mode=True

class PagesGet(BaseModel):
    id:int
    name:str
    pages_crud:list[PageCrud]
    class Config:
        orm_mode=True

class RolePermission(BaseModel):
    id:int
    pagecrud_id :int
    permission_crud:PageCrud
    class Config:
        orm_mode=True

class RolesGet(BaseModel):
    id:int
    name:str
    #role_permission : list[RolePermission]
    class Config:
        orm_mode=True
class User(BaseModel):
    username:Optional[str]=None
    status:int
    created_at:datetime
    full_name:Optional[str]=None
    is_client:Optional[int]=None
    id:int
    role_id:Optional[int]=None
    phone_number:Optional[str]=None
    user_role :Optional[RolesGet]=None
    class Config:
        orm_mode=True


class RolesGetMe(BaseModel):
    id:int
    name:str
    role_permission :list[int]
    class Config:
        orm_mode=True

class UserMe(BaseModel):
    username:Optional[str]=None
    status:int
    created_at:datetime
    full_name:Optional[str]=None
    is_client:Optional[int]=None
    id:int
    role_id:Optional[int]=None
    phone_number:Optional[str]=None
    user_role :Optional[RolesGet]=None
    
    class Config:
        orm_mode=True
class UserBaseme(BaseModel):
    user:User
    permissions:Optional[Dict[str,bool]]=None
    class Config:
        orm_mode=True



class UserInsertSch(BaseModel):
    username:str
    password:str
    phone_number:Optional[str]=None
    role_id:Optional[int]=None
    full_name:Optional[str]=None
    status:Optional[int]=None
    @validator('password')
    def validate_password_length(cls, password):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return password


class UserUpdate(BaseModel):
    id:int
    username:Optional[str]=None
    status:Optional[int]=None
    full_name:Optional[str]=None
    role_id:Optional[int]=None
    phone_number:Optional[int]=None
    password:Optional[str]=None
    class Config:
        orm_mode=True

    @validator('password')
    def validate_password_length(cls, password):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return password
    

class RolesCreate(BaseModel):
    name:str






    

    
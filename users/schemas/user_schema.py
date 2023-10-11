from pydantic import BaseModel,validator
from typing import Optional
from datetime import datetime
class User(BaseModel):
    username:Optional[str]=None
    status:int
    created_at:datetime
    id:int
    phone_number:Optional[str]=None
    class Config:
        orm_mode=True


class UserInsertSch(BaseModel):
    username:str
    password:str
    phone_number:Optional[str]=None
    @validator('password')
    def validate_password_length(cls, password):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return password


class UserFullBack(BaseModel):
    id:int
from typing import Optional ,Literal
from pydantic import BaseModel,Field
from pydantic import validator
from users.schemas.user_schema import User

class CreateCategory(BaseModel):
    name :str
    price:float
    


class GetCategory(BaseModel):
    name:Optional[str]=None
    price:Optional[float]=None
    id:Optional[int]=None
    status:int
    class Config:
        orm_mode=True



class CreateSubCat(BaseModel):
    name:str
    category_id:int
    contenttype_id:int
    class Config:
        orm_mode=True


class GetContentType(BaseModel):
    id:int
    name:str
    status:int
    class Config:
        orm_mode=True



class GetSubCat(BaseModel):
    id:int
    name:str
    category_id:int
    contenttype_id:int
    subcategory_vs_category:Optional[GetCategory]=None
    subcategory_vs_contenttype:Optional[GetContentType]=None
    class Config:
        orm_mode=True


class UpdateSubCat(BaseModel):
    id:int
    contenttype_id:Optional[int]=None
    name:Optional[str]=None
    status:Optional[int]=None
    class Config:
        orm_mode=True


class SelectValueCreate(BaseModel):
    content:str
    value:Optional[str]=None
    subcat_id:int



class SelectViewGet(BaseModel):
    id:int
    content: str
    value:Optional[str]=None
    selval_vs_subcat:GetSubCat
    class Config:
        orm_mode=True




class SelValFilter(BaseModel):
    id:Optional[int]=None
    content:Optional[str]=None
    value:Optional[str]=None
    status:Optional[int]=None
    subcat_id:Optional[int]=None
    


class UpdateSelectValue(BaseModel):
    id:int
    content:Optional[str]=None
    value:Optional[str]=None
    status:Optional[int]=None


class ChildSelCreate(BaseModel):
    selval_id:int
    content:str
    value:Optional[str]=None





class GetChildSelVal(BaseModel):
    id:int
    selval_id:int
    content:str
    value:Optional[str]=None
    childselval_vs_selval:SelectViewGet
    class Config:
        orm_mode=True



class FilterChildSelVal(BaseModel):
    id:Optional[int]=None
    selval_id:Optional[int]=None
    content :Optional[str]=None
    value:Optional[str]=None
    status:Optional[int]=None

class UpdateChildSelVal(BaseModel):
    id:int
    content:Optional[str]=None
    value:Optional[str]=None
    status:Optional[int]=None




class GetChildSelValWithId(BaseModel):
    id:int
    content:Optional[str]=None
    value:Optional[str]=None
    status:Optional[int]=None
    class Config:
        orm_mode=True



class SelectViewGetWithId(BaseModel):
    id:int
    content: str
    value:Optional[str]=None
    status:int
    selval_vs_childselval:Optional[list[GetChildSelValWithId]]=None
    class Config:
        orm_mode=True


class GetSubCatWithId(BaseModel):
    id:int
    name:str
    category_id:Optional[int]=None
    contenttype_id:Optional[int]=None
    status:int 
    subcat_vs_selval:Optional[list[SelectViewGetWithId]]=None
    subcategory_vs_contenttype:Optional[GetContentType]=None
    class Config:
        orm_mode=True


class GetCategoryWithId(BaseModel):
    name:Optional[str]=None
    price:Optional[float]=None
    id:Optional[int]=None
    status:int
    category_vs_subcategory:list[GetSubCatWithId]
    class Config:
        orm_mode=True


class GetOrdervsId(BaseModel):
    id:int
    order_vs_user:User
    order_vs_category:GetCategory
    class Config:
        orm_mode=True

class OrderFromValue(BaseModel):
    id:int
    content:Optional[str]
    order_id:int
    subcat_id:int
    value_vs_subcat:GetSubCat
    select_id:Optional[int]=None
    value_vs_select:Optional[SelectViewGet]=None
    selchild_id:Optional[int]=None
    value_vs_selchild:Optional[GetChildSelValWithId]=None
    class Config:
        orm_mode=True


class BaseOrder(BaseModel):
    order:list[GetOrdervsId]
    value:list[OrderFromValue]
    class Config:
        orm_mode=True 


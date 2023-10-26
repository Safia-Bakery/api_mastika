from typing import Optional ,Literal,Dict
from pydantic import BaseModel,Field
from pydantic import validator
from users.schemas.user_schema import User
from uuid import UUID
from datetime import datetime

class CreateCategory(BaseModel):
    name :str
    


class GetCategory(BaseModel):
    name:Optional[str]=None
    id:Optional[int]=None
    image:Optional[str]=None
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

class FillingAddGet(BaseModel):
    name:Optional[str]=None
    category_id:Optional[int]=None
    ptype:Optional[int]=None
    class Config:
        orm_mode=True



class FillingGet(BaseModel):
    id:int
    name:str
    category_id:int
    ptype:int
    class Config:
        orm_mode=True


class FillingUpdate(BaseModel):
    id:int
    name:Optional[str]=None
    status:Optional[str]=None
    ptype:Optional[int]=None



class GetCategoryWithId(BaseModel):
    name:Optional[str]=None
    id:Optional[int]=None
    status:int
    c_filling:Optional[list[FillingGet]]=None
    category_vs_subcategory:list[GetSubCatWithId]=None
    class Config:
        orm_mode=True


class ProductsFilter(BaseModel):
    id:UUID
    status:int
    name:str
    productType:str
    group_id:UUID
    price:Optional[float]=None
    class Config:
        orm_mode=True

class GetBranchs(BaseModel):
    id:UUID
    name:str
    latitude:Optional[float]=None
    langtitude:Optional[float]=None
    country:Optional[str]=None
    status:int
    is_fabrica:Optional[int]=None
    class Config:
        orm_mode=True

class GetDepartments(BaseModel):
    id:UUID
    name:str
    branch_id:UUID
    origin:int
    status:int
    branch_dr:Optional[GetBranchs]=None
    class Config:
        orm_mode=True


class OrderProductsGet(BaseModel):
    id:Optional[int]=None
    order_vs_product:ProductsFilter
    product_id:Optional[UUID]=None
    comment:Optional[str]=None
    amount:Optional[int]=None
    floor:Optional[int]=None
    portion:Optional[int]=None
    class Config:
        orm_mode=True

class OrderFillingGet(BaseModel):
    id:int
    filling_id:int
    floor:int
    filler:Optional[FillingGet]=None
    class Config:
        orm_mode=True

class GetOrdervsId(BaseModel):
    id:int
    order_user:Optional[str]=None
    order_vs_user:User
    phone_number:Optional[str]=None
    extra_number:Optional[str]=None
    payment_type:Optional[int]=None
    firstly_payment:Optional[int]=None
    is_delivery:Optional[int]=None
    comment:Optional[str]=None
    reject_reason:Optional[str]=None
    created_at:datetime
    updated_at:Optional[datetime]=None
    deliver_date:Optional[datetime]=None
    status:int
    #product_order:Optional[list[OrderProductsGet]]=None
    address:Optional[str]=None
    apartment:Optional[str]=None
    home:Optional[str]=None
    near_to:Optional[str]=None
    order_vs_category:Optional[GetCategory]=None
    lat : Optional[str]=None
    complexity :Optional[int]=None
    long:Optional[str]=None
    order_br:Optional[GetDepartments]=None
    product_order:Optional[list[OrderProductsGet]]=None
    order_fill:Optional[list[OrderFillingGet]]
    packaging:Optional[int]=None
    images:Optional[list[str]]=None
    class Config:
        orm_mode=True



class OrderFromValue(BaseModel):
    id:int
    content:Optional[str]=None
    order_id:Optional[int]=None
    subcat_id:Optional[int]=None
    value_vs_subcat:Optional[GetSubCat]=None
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

class Departments_get(BaseModel):
    id:UUID
    name:str
    origin:int
    status:int
    class Config:
        orm_mode=True 

class Branches_list(BaseModel):
    id:UUID
    name:str
    latitude:Optional[float]=None
    longtitude:Optional[float]=None
    country :str
    status:int
    is_fabrica:Optional[int]=None
    department_br:list[Departments_get]
    class Config:
        orm_mode=True 


class GroupsGet(BaseModel):
    id:UUID
    name:str
    code:str
    status:int
    class Config:
        orm_mode=True


class OrderCreation(BaseModel):
    order_user : str
    phone_number :Optional[str]=None
    extra_number: Optional[str]=None
    payment_type:Optional[int]=None
    firstly_payment:Optional[int]=None
    is_delivery:int
    comment :Optional[str]=None
    deliver_date:Optional[datetime]=None
    address:Optional[str]=None
    apartment:Optional[str]=None
    home:Optional[str]=None
    near_to:Optional[str]=None
    department_id:Optional[UUID]=None
    category_id:Optional[int]=None
    lat:Optional[str]=None
    long:Optional[str]=None
    complexity:Optional[int]=None
    filler:Optional[Dict[str,Dict[str,str]]]=None
    packaging:Optional[int]=None
    images:Optional[list[str]]=None




class OrderUpdate(BaseModel):
    id :int
    order_user : Optional[str]=None
    phone_number :Optional[str]=None
    extra_number: Optional[str]=None
    payment_type:Optional[int]=None
    firstly_payment:Optional[int]=None
    is_delivery:Optional[int]=None
    comment :Optional[str]=None
    deliver_date:Optional[datetime]=None
    address:Optional[str]=None
    apartment:Optional[str]=None
    home:Optional[str]=None
    near_to:Optional[str]=None
    department_id:Optional[UUID]=None
    category_id:Optional[int]=None
    status:Optional[int]=None
    lat:Optional[str]=None
    long:Optional[str]=None
    reject_reason:Optional[str]=None
    complexity :Optional[int]=None


class OrderProducts(BaseModel):
    order_id:int
    product_id:UUID
    comment:Optional[str]=None
    amount:int
    floor:Optional[int]=None
    portion :Optional[int]=None


class OrderProductUpdate(BaseModel):
    id:int
    comment:Optional[str]=None
    amount:Optional[int]=None
    floor:Optional[int]=None
    portion:Optional[int]=None









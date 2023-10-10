from sqlalchemy.orm import Session
from apis.schemas import api_schema
from apis.models import models
from typing import Optional
from sqlalchemy.orm import joinedload


def create_cat(db:Session,name,price,iiko_id):
    query = models.Category(name=name,price=price,iiko_id=iiko_id)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def get_category_withid(db:Session,id:int):
    query = db.query(models.Category).filter(models.Category.id==id).options(joinedload(models.Category.category_vs_subcategory)).filter(models.SubCategory.status==0).first()
    return query


def get_category(db:Session,id:Optional[int]=None,name:Optional[str]=None,price:Optional[float]=None,status:Optional[int]=None):
    query = db.query(models.Category)
    if id is not None:
        query  = query.filter(models.Category.id==id)
    if name is not None:
        query = query.filter(models.Category.name.ilike(f"%{name}%"))
    if price is not None:
        query = query.filter(models.Category.price.ilike(f"%{price}%"))
    if status is not None:
        query = query.filter(models.Category.status==status)
    return query.all()

def get_categories_iiko(db:Session):
    query = db.query(models.Category).all()
    return query



def update_category(db:Session,form_data:api_schema.GetCategory):
    query = db.query(models.Category).filter(models.Category.id==form_data.id).first()
    if query:
        if form_data.status is not None:
            query.status=form_data.status
        if form_data.name is not None:
            query.name = form_data.name
        if form_data.price is not None:
            query.price = form_data.price

        db.commit()
        db.refresh(query)
    return query



def get_content_types(db:Session):
    query = db.query(models.ContentType).all()
    return query




def sub_create(db:Session,form_data:api_schema.CreateSubCat):
    query = models.SubCategory(name=form_data.name,category_id=form_data.category_id,contenttype_id=form_data.contenttype_id) 
    db.add(query)
    db.commit()
    db.refresh(query)
    return query




def filter_subcategory(db:Session,id:Optional[int]=None,name:Optional[str]=None,category_id:Optional[str]=None):
    query =db.query(models.SubCategory)
    if id is not None:
        query = query.filter(models.SubCategory.id==id)
    if name is not None:
        query = query.filter(models.SubCategory.name.ilike(f"%{name}%"))
    if category_id is not None:
        query = query.filter(models.SubCategory.category_id==category_id)
    return query.all()
    


def update_subcategory(db:Session,form_data:api_schema.UpdateSubCat):
    query = db.query(models.SubCategory).filter(models.SubCategory.id==form_data.id).first()
    if query:
        if form_data.contenttype_id is not None:
            query.contenttype_id=form_data.contenttype_id
        if form_data.name is not None:
            query.name = form_data.name
        if form_data.status is not None:
            query.status = form_data.status
        db.commit()
        db.refresh(query)
    return query

def create_selectvl(db:Session,form_data:api_schema.SelectValueCreate):
    query = models.SelectValues(content=form_data.content,value=form_data.value,subcat_id=form_data.subcat_id)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def get_selval(db:Session,id,content,value,status,subcat_id):
    query = db.query(models.SelectValues)
    if content is not None:
        query = query.filter(models.SelectValues.content.ilike(f"%{content}%"))
    if id is not None:
        query = query.filter(models.SelectValues.id==id)
    if value is not None:
        query = query.filter(models.SelectValues.value.ilike(f"%{value}%"))
    if status is not None:
        query = query.filter(models.SelectValues.status==status)
    if subcat_id is not None:
        query = query.filter(models.SelectValues.subcat_id==subcat_id)
    return query.all()



def update_select_value(db:Session,form_data:api_schema.UpdateSelectValue):
    query = db.query(models.SelectValues).filter(models.SelectValues.id==form_data.id).first()
    if form_data.content is not None:
        query.content = form_data.content
    if form_data.value is not None:
        query.value = form_data.value
    if form_data.status is not None:
        query.status = form_data.status
    db.commit()
    db.refresh(query)
    return query


def create_childselect(db:Session,form_data:api_schema.ChildSelCreate):
    query = models.ChildSelVal(content=form_data.content,selval_id=form_data.selval_id,value=form_data.value)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def filter_child_selval(db:Session,content,value,selval_id,status,id):
    query = db.query(models.ChildSelVal)
    if content is not None:
        query = query.filter(models.ChildSelVal.content.ilike(f"%{content}%"))
    if value is not None:
        query = query.filter(models.ChildSelVal.value.ilike(f"%{value}%"))
    if selval_id is not None:
        query = query.filter(models.ChildSelVal.selval_id==selval_id)
    if status is not None:
        query = query.filter(models.ChildSelVal.status==status)
    if id is not None:
        query = query.filter(models.ChildSelVal.id==id)
    return query.all()

def update_child_selvalue(db:Session,form_data:api_schema.UpdateChildSelVal):
    query = db.query(models.ChildSelVal).filter(models.ChildSelVal.id==form_data.id).first()
    if form_data.content is not None:
        query.content =form_data.content
    if form_data.status is not None:
        query.status = form_data.status
    if form_data.value is not None:
        query.value = form_data.value
    db.commit()
    db.refresh(query)
    return query


def create_order(db:Session,category_id,user_id):
    query = models.Order(category_id=category_id,user_id=user_id)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def create_value_order(db:Session,table):
    table = table
    db.add(table)
    db.commit()
    db.refresh(table)
    return table


def get_order_with_id(db:Session,id):
    query = db.query(models.Order).filter(models.Order.id==id).all()
    return query


def get_values_oforder(db:Session,id):
    query = db.query(models.Value).filter(models.Value.order_id==id).all()
    return query

def getOrderList(db:Session):
    query = db.query(models.Order).all()
    return query

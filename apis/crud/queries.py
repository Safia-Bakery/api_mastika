from sqlalchemy.orm import Session
from apis.schemas import api_schema
from apis.models import models
from typing import Optional
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from sqlalchemy import cast, Date


def create_cat(db:Session,name,image):
    try:
        query = models.Category(name=name,image=image)
        db.add(query)
        db.commit()
        db.refresh(query)
        return query
    except IntegrityError as e:
        # Handle unique constraint violation
        db.rollback()
        return "Error: Unique constraint violation."

def get_category_withid(db:Session,id:int):
    query = db.query(models.Category).filter(models.Category.id==id).first()
    return query


def get_category(db:Session,id:Optional[int]=None,name:Optional[str]=None,status:Optional[int]=None):
    query = db.query(models.Category)
    if id is not None:
        query  = query.filter(models.Category.id==id)
    if name is not None:
        query = query.filter(models.Category.name.ilike(f"%{name}%"))
    if status is not None:
        query = query.filter(models.Category.status==status)
    return query.all()

def get_categories_iiko(db:Session):
    query = db.query(models.Category).all()
    return query



def update_category(db:Session,name,status,image,id):
    query = db.query(models.Category).filter(models.Category.id==id).first()
    if query:
        if status is not None:
            query.status=status
        if name is not None:
            query.name = name
        if image is not None:
            query.image=image

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



def create_order(db:Session,user_id,form_data:api_schema.OrderCreation):
    if form_data.department_id is not None:
        try:
            department_id = db.query(models.Departments).filter(models.Departments.branch_id==form_data.department_id).first().id
        except:
            department_id = None
    else:
        department_id = None
    query = models.Order(order_user=form_data.order_user,phone_number=form_data.phone_number,extra_number=form_data.extra_number,payment_type=form_data.payment_type,
                         firstly_payment=form_data.firstly_payment,
                         is_delivery=form_data.is_delivery,
                         comment=form_data.comment,
                         deliver_date=form_data.deliver_date,
                         address=form_data.address,
                         apartment=form_data.apartment,
                         home=form_data.home,
                         near_to=form_data.near_to,
                         department_id=department_id,
                         user_id=user_id,
                         category_id=form_data.category_id,
                         lat=form_data.lat,
                         long=form_data.long,
                         complexity =form_data.complexity,
                         packaging=form_data.packaging,
                         images=form_data.images,
                         color=form_data.color,
                         color_details=form_data.color_details,
                         floor=form_data.floor,
                         portion=form_data.portion)


    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def update_order(db:Session,form_data:api_schema.OrderUpdate):
    query = db.query(models.Order).filter(models.Order.id==form_data.id).first()
    if query:
        
        if form_data.order_user is not None:
            query.order_user= form_data.order_user
        if form_data.phone_number is not None:
            query.phone_number = form_data.phone_number
        if form_data.extra_number is not None:
            query.extra_number = form_data.extra_number
        if form_data.payment_type is not None:
            query.payment_type =form_data.payment_type
        if form_data.firstly_payment is not None:
            query.firstly_payment =form_data.firstly_payment
        if form_data.is_delivery is not None:
            query.is_delivery = form_data.is_delivery
        if form_data.comment is not None:
            query.comment = form_data.comment
        if form_data.deliver_date is not None:
            query.deliver_date = form_data.deliver_date
        if form_data.address is not None:
            query.address = form_data.address
        if form_data.apartment is not None:
            query.apartment = form_data.apartment
        if form_data.home is not None:
            query.home = form_data.home
        if form_data.near_to is not None:
            query.near_to = form_data.near_to
        if form_data.department_id  is not None:
            query.department_id = form_data.department_id
        if form_data.category_id is not None:
            query.category_id =form_data.category_id
        if form_data.status is not None:
            query.status = form_data.status
        if form_data.lat is not None:
            query.lat = form_data.lat
        if form_data.long is not None:
            query.long = form_data.long
        if form_data.reject_reason is not None:
            query.reject_reason = form_data.reject_reason
        if form_data.complexity is not None:
            query.complexity =form_data.complexity
        if form_data.floor is not None:
            query.floor = form_data.floor
        if form_data.portion is not None:
            query.portion = form_data.portion
        if form_data.color is not None:
            query.color =form_data.color
        if form_data.color_details is not None:
            query.color_details=form_data.color_details
        if form_data.images is not None:
            query.images=form_data.images
        if form_data.packaging is not None:
            query.packaging =form_data.packaging
        db.commit()
        db.refresh(query)
    
    return query



def create_order_products(db:Session,form_data:api_schema.OrderProducts):
    query = models.OrderProducts(order_id=form_data.order_id,product_id=form_data.product_id,comment=form_data.comment,amount=form_data.amount,floor=form_data.floor,portion=form_data.portion)
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

def getOrderList(db:Session,status,cake,is_delivery,created_at,branch_id):
    query = db.query(models.Order)
    if status is not None:
        query = query.filter(models.Order.status==status)
    if cake is not None:
        query = query.filter(models.OrderProducts.product_id==cake)
    if is_delivery is not None:
        query = query.filter(models.Order.is_delivery==is_delivery)
    if created_at is not None:
        query = query.filter(cast(models.Order.created_at,Date)==created_at)
    if branch_id is not None:
        query = query.filter(models.Departments.branch_id==branch_id)
    return query.order_by(models.Order.id.desc()).all()



def insert_branches(db:Session,items):
    for item in items:
        try:
            new_item = models.Branchs(country='Uzbekistan', name=item[0],status=1,id=item[1])
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
        except:
            db.rollback()
            return "Error: Unique constraint violation."
    return True

def insert_departments(db:Session,items):
    for item in items:
        try:
            new_item = models.Departments( name=item[0],status=1,id=item[1],branch_id=item[2])
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
        except:
            db.rollback()
            return "Error: Unique constraint violation."
    return True


def get_branches_list(db:Session,id):
    query = db.query(models.Branchs)
    if id is not None:
        query = query.filter(models.Branchs.id==id)
    return query.all()


def get_dep_with_branch(db:Session,id):
    query = db.query(models.Departments).filter(models.Departments.branch_id==id).first()
    return query

def add_product_groups(db:Session,id,code,name):
    try:
        query = models.Groups(name=name,code=code,id=id)
        db.add(query)
        db.commit()
        return True
    except:
            db.rollback()
            return "Error: Unique constraint violation."
    
def add_products(db:Session,id,name,producttype,groud_id,price):
    try:
        query = models.Products(id=id,name=name,productType=producttype,group_id=groud_id,price=price)
        db.add(query)
        db.commit()
        return True
    except:
        db.rollback()
        return "Error: Unique constraint violation."

def get_product_groups(db:Session,id:Optional[UUID]=None,name:Optional[str]=None):
    query = db.query(models.Groups)
    if id is not None:
        query = query.filter(models.Groups.id==id)   
    if name is not None:
        query = query.filter(models.Groups.name.ilike(f"%{name}%"))  
    return query.all()

def get_products(db:Session,id:Optional[UUID]=None,group_id:Optional[UUID]=None,status:Optional[int]=None,name:Optional[str]=None):
    query = db.query(models.Products)
    if id is not None:
        query = query.filter(models.Products.id==id)
    if group_id is not None:
        query = query.filter(models.Products.group_id==group_id)
    if status is not None:
        query = query.filter(models.Products.status==status)
    if name is not None:
        query = query.filter(models.Products.name.ilike(f"%{name}%"))
    return query.all()



def get_subcategory_with_id(db:Session,id):
    query = db.query(models.SubCategory).filter(models.SubCategory.id==id).first()
    return query


def update_order_product(db:Session,form_data:api_schema.OrderProductUpdate):
    query = db.query(models.OrderProducts).filter(models.OrderProducts.id==form_data.id).first()
    if query:
        if form_data.amount is not None:
            query.amount = form_data.amount
        if form_data.comment is not None:
            query.comment = form_data.comment
        if form_data.floor is not None:
            query.floor = form_data.floor
        if form_data.portion is not None:
            query.portion=form_data.portion
        db.commit()
    
    return query


def add_filling(db:Session,form_data:api_schema.FillingAddGet):
    query = models.Fillings(name=form_data.name,ptype=form_data.ptype,category_id=form_data.category_id)
    db.add(query)
    db.commit()
    db.refresh(query)

    return query

def update_filling(db:Session,form_data:api_schema.FillingUpdate):
    query = db.query(models.Fillings).filter(models.Fillings.id==form_data.id).first()
    if query:
        if form_data.name is not None:
            query.name=form_data.name
        if form_data.status is not None:
            query.status = form_data.status
        if form_data.ptype is not None:
            query.ptype=form_data.ptype
        db.commit()
    return query

def get_filling(db:Session,id,ptype,status,name,category_id):
    query = db.query(models.Fillings)
    if id is not None:
        query = query.filter(models.Fillings.id==id)
    if ptype is not None:
        query = query.filter(models.Fillings.ptype==ptype)
    if status is not None:
        query = query.filter(models.Fillings.status==status)
    if name is not None:
        query = query.filter(models.Fillings.name.ilike(f"%{name}%"))
    if category_id is not None:
        query = query.filter(models.Fillings.category_id==category_id)
    return query.all()


def add_order_filling(db:Session,order_id,filling_id,floor):
    query = models.OrderFilling(order_id=order_id,filling_id=filling_id,floor=floor)
    db.add(query)
    db.commit()
    return True
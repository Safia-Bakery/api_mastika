from sqlalchemy import Column, Integer, String,ForeignKey,Float,DateTime,Boolean,BIGINT,Table,VARCHAR,CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import pytz 
from sqlalchemy.dialects.postgresql import UUID
from users.models.models import Base
import uuid



class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(VARCHAR(length=255))
    status = Column(Integer,default=1)
    category_vs_order = relationship('Order',back_populates='order_vs_category')
    category_vs_subcategory = relationship('SubCategory',back_populates='subcategory_vs_category')


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer,primary_key=True,index=True)
    phone_number = Column(String,nullable=True)
    location = Column(String,nullable=True)
    department_id = Column(UUID(as_uuid=True),ForeignKey('departments.id'),nullable=True)
    order_br = relationship('Departments',back_populates='department_br')
    user_id = Column(Integer,ForeignKey('users.id'))
    order_vs_user = relationship('Users',back_populates='user_vs_order')
    category_id = Column(Integer,ForeignKey('categories.id'))
    order_vs_category = relationship('Category',back_populates='category_vs_order')
    order_vs_value = relationship('Value',back_populates='value_vs_order')







class ContentType(Base):
    __tablename__ = 'content_types'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(VARCHAR(255))
    status = Column(Integer,default=1)
    contenttype_vs_subcategory = relationship('SubCategory',back_populates='subcategory_vs_contenttype')



class SubCategory(Base):
    __tablename__  = 'sub_categories'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    category_id = Column(Integer,ForeignKey('categories.id'))
    status = Column(Integer,default=1)
    subcategory_vs_category = relationship('Category',back_populates='category_vs_subcategory')
    contenttype_id = Column(Integer,ForeignKey('content_types.id'))
    subcategory_vs_contenttype = relationship('ContentType',back_populates='contenttype_vs_subcategory')
    subcat_vs_value = relationship('Value',back_populates='value_vs_subcat')
    subcat_vs_selval = relationship('SelectValues',back_populates='selval_vs_subcat')



class SelectValues(Base):
    __tablename__ = 'select_values'
    id =Column(Integer,primary_key=True,index=True)
    content = Column(String)
    value = Column(VARCHAR(length=255),nullable=True)
    status = Column(Integer,default=1)
    subcat_id = Column(Integer,ForeignKey('sub_categories.id'))
    selval_vs_subcat = relationship('SubCategory',back_populates='subcat_vs_selval')
    selval_vs_childselval = relationship('ChildSelVal',back_populates='childselval_vs_selval')
    select_vs_value = relationship('Value',back_populates='value_vs_select')





class ChildSelVal(Base):
    __tablename__ = 'childsel_values'
    id = Column(Integer,primary_key=True,index=True)
    selval_id = Column(Integer,ForeignKey('select_values.id'))
    childselval_vs_selval= relationship('SelectValues',back_populates='selval_vs_childselval')
    content = Column(VARCHAR(length=255))
    value = Column(String,nullable=True)
    status = Column(Integer,default=1)
    selchild_vs_value = relationship('Value',back_populates='value_vs_selchild')







class Value(Base):
    __tablename__ = 'values'
    id = Column(Integer,primary_key=True,index=True)
    content = Column(String,nullable=True)
    order_id = Column(Integer,ForeignKey('orders.id'))
    value_vs_order = relationship('Order',back_populates='order_vs_value')
    subcat_id = Column(Integer,ForeignKey('sub_categories.id'))
    value_vs_subcat = relationship('SubCategory',back_populates='subcat_vs_value')
    select_id = Column(Integer,ForeignKey('select_values.id'),nullable=True)
    value_vs_select = relationship('SelectValues',back_populates='select_vs_value')
    selchild_id = Column(Integer,ForeignKey('childsel_values.id'),nullable=True)
    value_vs_selchild = relationship('ChildSelVal',back_populates='selchild_vs_value')







class Branchs(Base):
    __tablename__='branchs'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name = Column(String)
    latitude = Column(Float,nullable=True)
    longtitude = Column(Float,nullable=True)
    country = Column(String,nullable=True)
    status = Column(Integer,default=0)
    department_br = relationship('Departments',back_populates='branch_dr')
    is_fabrica = Column(Integer,nullable=True)










class Departments(Base):
    __tablename__ = 'departments'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name = Column(String)
    department_br = relationship('Order',back_populates='order_br')
    branch_id = Column(UUID(as_uuid=True),ForeignKey('branchs.id'))
    branch_dr = relationship('Branchs',back_populates='department_br')
    origin = Column(Integer,default=0)
    status = Column(Integer,default=0)
    #supplier = relationship('Suppliers',back_populates='store')


class Groups(Base):
    __tablename__ = 'groups'
    id= Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name = Column(String)
    code=Column(String,nullable=True)
    group_r = relationship('Products',back_populates='product_r')
    status=Column(Integer,default=1)

class Products(Base):
    __tablename__ = 'products'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    status= Column(Integer,default=1)
    name = Column(String)
    productType = Column(String,nullable=True)
    group_id = Column(UUID(as_uuid=True),ForeignKey('groups.id'))
    product_r = relationship('Groups',back_populates='group_r')
    price = Column(Float,nullable=True)




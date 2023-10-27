from sqlalchemy import Column, Integer, String,ForeignKey,Float,DateTime,Boolean,BIGINT,Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import pytz 
from config.database import Base




class Pages(Base):
    __tablename__ = 'pages'
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    pages_crud = relationship('PageCrud',back_populates='crud_pages')

class PageCrud(Base):
    __tablename__='pagecrud'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    page_id = Column(Integer,ForeignKey('pages.id'))
    crud_pages = relationship('Pages',back_populates='pages_crud')
    crud_permission = relationship('Permissions',back_populates='permission_crud')


class Permissions(Base):
    __tablename__='permissions'
    id = Column(Integer,primary_key=True,index=True)
    pagecrud_id = Column(Integer,ForeignKey('pagecrud.id'))
    permission_crud = relationship('PageCrud',back_populates='crud_permission')
    role_id = Column(Integer,ForeignKey('roles.id'))
    permission_role = relationship('Roles',back_populates='role_permission')


class Roles(Base):
    __tablename__='roles'
    id = Column(Integer,primary_key=True,index=True)
    name= Column(String)
    status=Column(Integer,default=1)
    role_permission = relationship('Permissions',back_populates='permission_role')
    role_user = relationship('Users',back_populates='user_role')





class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True,nullable=True)
    password = Column(String,nullable=True)
    phone_number = Column(String,nullable=True)
    full_name = Column(String,nullable=True)
    created_at = Column(DateTime(timezone=True),default=func.now())
    status = Column(Integer,default=0)
    is_client = Column(Integer,default=0)
    user_vs_order = relationship('Order',back_populates='order_vs_user')
    role_id = Column(Integer,ForeignKey("roles.id"),nullable=True)
    user_role = relationship('Roles',back_populates='role_user')
    tel_id = Column(BIGINT,nullable=True)









    


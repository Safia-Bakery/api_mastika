from sqlalchemy import Column, Integer, String,ForeignKey,Float,DateTime,Boolean,BIGINT,Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import pytz 
from config.database import Base









class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True,nullable=True)
    password = Column(String,nullable=True)
    created_at = Column(DateTime(timezone=True),default=func.now())
    status = Column(Integer,default=0)
    user_vs_order = relationship('Order',back_populates='order_vs_user')


    


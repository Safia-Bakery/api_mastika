from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi import Depends, FastAPI, HTTPException,UploadFile,File,Form,Header,Request,status
from typing import Optional
from config.database import engine
from users.routers.user_router import user_router
from apis.routers.api_router import api_router
from fastapi_pagination import paginate,Page,add_pagination
from apis.models.models import Base

app = FastAPI()
app.title = "Safia FastApi App"
app.version = "0.0.1"
app.include_router(user_router)
app.include_router(api_router)
Base.metadata.create_all(bind=engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Home"])
def message():
    """message get method"""
    return HTMLResponse("<h1>Fuck of man!</h1>")



add_pagination(app)
add_pagination(api_router)
add_pagination(user_router)
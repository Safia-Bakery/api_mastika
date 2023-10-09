import os 
from dotenv import load_dotenv
from passlib.context import CryptContext
import bcrypt
from datetime import datetime,timedelta
from users.schemas.user_schema import User
from typing import Union,Any
from users.crud.queries import UserService
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from config.database import SessionLocal
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')   # should be kept secret
JWT_REFRESH_SECRET_KEY =  os.environ.get('JWT_REFRESH_SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)





def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))



def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



async def get_current_user(token: str = Depends(reuseable_oauth),db:Session=Depends(get_db)) -> User:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        expire_date = payload.get('exp')
        sub = payload.get('sub')
        if datetime.fromtimestamp(expire_date) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user: Union[dict[str, Any], None] = UserService(db).get_user(sub)
    
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return user




def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt
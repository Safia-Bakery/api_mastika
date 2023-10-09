from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from users.schemas.user_schema import UserInsertSch,User
from users.utils.user_micro import get_db,hash_password,get_current_user,verify_password,create_access_token,create_refresh_token
from users.crud.queries import UserService
from fastapi_pagination import paginate,Page,add_pagination
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

user_router = APIRouter()
@user_router.post('/user',tags=['Users'],response_model=User)
async def create_user(form_data:UserInsertSch,db:Session=Depends(get_db)):
    try:
        password  = hash_password(password=form_data.password)
        query  = UserService(db).create_user(form_data.username,password=password)
        return query
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user already exist"
        )

@user_router.post('/login',tags=['Users'])
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    user = UserService(db).get_user(username=form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
    }



@user_router.get('/user',tags=['Users'],response_model=Page[User])
async def get_user(db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = UserService(db).get_users()
    return paginate(query)



@user_router.get('/me',tags=['Users'],response_model=User)
async def get_user(db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    return request_user
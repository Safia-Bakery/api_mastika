from fastapi import APIRouter
from sqlalchemy.orm import Session
from users.models.models import Permissions
from fastapi import Depends,HTTPException,status
from users.schemas.user_schema import UserInsertSch,User,UserUpdate,RolesCreate,RolesGet,PagesGet,UserMe,UserBaseme
from users.utils.user_micro import get_db,hash_password,get_current_user,verify_password,create_access_token,create_refresh_token
from users.crud.queries import UserService
from fastapi_pagination import paginate,Page,add_pagination
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Optional

user_router = APIRouter()
@user_router.post('/user',tags=['Users'],response_model=User)
async def create_user(form_data:UserInsertSch,db:Session=Depends(get_db)):
    try:
        phone_number = form_data.phone_number.replace('+','')
        user = UserService(db).get_user_withph(phone_number=phone_number)
        if user:
            return user
        password  = hash_password(password=form_data.password)
        query  = UserService(db).create_user(form_data.username,password=password,phone_number=phone_number,full_name=form_data.full_name,status=form_data.status,role_id=form_data.role_id)
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
    if user.role_id is None and user.status!=2:
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
async def get_user(is_client:Optional[int]=None,id:Optional[int]=None,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = UserService(db).get_users(id=id,is_client=is_client)
    return paginate(query)



@user_router.get('/me',tags=['Users'],response_model=UserBaseme)
async def get_user(db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    if request_user.status==2:
        data = {str(i.id):True for i in UserService(db=db).all_permissions()}

        user = {'user':request_user,'permissions':data}
        return user
    if request_user.user_role is not None:
        data = {str(i.pagecrud_id):True for i in request_user.user_role.role_permission}
        user = {'user':request_user,'permissions':data}
        return user
    else:
        user = {'user':request_user}
        return user

@user_router.get('/user/get/create',tags=['users'],response_model=User)
async def get_or_create(phone_number:str,db:Session=Depends(get_db)):
    phone_number = phone_number.replace('+','')
    query =UserService(db).get_or_create(phone_number=phone_number)
    return query

@user_router.put('/users',tags=['Users'],response_model=User)
async def update_user(form_data:UserUpdate,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = UserService(db).user_update(form_data=form_data)
    return query

@user_router.put('/roles',tags=['Users'])
async def update_user_permissions(role_id:int,per_list:Optional[list[int]]=None,name:Optional[str]=None,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    if per_list is not None:
        UserService(db).set_null_permissions(id=role_id)
        permisison = [Permissions(role_id=role_id,pagecrud_id=i) for i in per_list]
        UserService(db).def_add_permissions(permisison)
    if name is not None:
        query = UserService(db).role_update(name=name,role_id=role_id)
    return {'success':True}
@user_router.post('/roles',response_model=RolesGet,tags=['Users'])
async def role_create(form_data:RolesCreate,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = UserService(db).create_role(name=form_data.name)
    return query


@user_router.get('/roles',response_model=list[RolesGet],tags=['Users'])
async def get_roles_list(id:Optional[int]=None,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = UserService(db).get_roles(id)
    return query

@user_router.get('/pages',response_model=list[PagesGet],tags=['Users'])
async def get_pages(db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = UserService(db).get_pages()
    return query









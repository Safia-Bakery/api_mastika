from apis.schemas import api_schema
from fastapi import APIRouter
from users.utils.user_micro import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from apis.crud import queries
from users.schemas.user_schema import User
from users.utils.user_micro import get_current_user
from typing import Optional,Union
from apis.utils.api_micro import authiiko,get_cakes,generate_random_filename,list_departments,list_stores
from fastapi import Request
import shutil
from fastapi_pagination import paginate,Page,add_pagination
import re
from apis.models import models

mastika  = '30ed6a72-8771-4c81-91ad-e4b71305858d'

api_router = APIRouter()


@api_router.post('/v1/category')
async def create_category(form_data:api_schema.CreateCategory,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    #query = queries.create_cat(db=db,form_data=form_data)
    return {'success':True,'message':'this api currently inactive you data  will not be added to category list'}


@api_router.get('/v1/category',response_model=list[api_schema.GetCategory])
async def get_filter_category(name:Optional[str]=None,id:Optional[int]=None,status:Optional[int]=None,price:Optional[float]=None,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    query = queries.get_category(db=db,name=name,id=id,price=price,status=status)
    return query

@api_router.put('/v1/category',response_model=api_schema.GetCategory)
async def update_category(form_data:api_schema.GetCategory,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    query = queries.update_category(form_data=form_data,db=db)
    return query





@api_router.get('/v1/content/types')
async def get_content(db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.get_content_types(db=db)
    return query


@api_router.post('/v1/sub/category')
async def create_subcategory(form_data:api_schema.CreateSubCat,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.sub_create(db=db,form_data=form_data)
    return query


@api_router.get('/v1/sub/category',response_model=list[api_schema.GetSubCat])
async def filter_subcategory(id:Optional[int]=None,name:Optional[str]=None,category_id:Optional[int]=None,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.filter_subcategory(db=db,id=id,name=name,category_id=category_id)
    return query

@api_router.put('/v1/sub/category')
async def update_subcategory(form_data:api_schema.UpdateSubCat,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.update_subcategory(db=db,form_data=form_data)
    return query


@api_router.post('/v1/sel/value')
async def create_sel_value(form_data:api_schema.SelectValueCreate,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.create_selectvl(db=db,form_data=form_data)
    return query


@api_router.get('/v1/sel/value',response_model=list[api_schema.SelectViewGet])
async def filter_select_val(id:Optional[int]=None,content:Optional[str]=None,value:Optional[str]=None,status:Optional[int]=None,subcat_id:Optional[int]=None,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.get_selval(db=db,id=id,content=content,value=value,status=status,subcat_id=subcat_id)
    return query


@api_router.put('/v1/sel/value',response_model=api_schema.SelectViewGet)
async def update_select_val(form_data:api_schema.UpdateSelectValue,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query= queries.update_select_value(db=db,form_data=form_data)
    return query



@api_router.post('/v1/child/sel/value',response_model=api_schema.GetChildSelVal)
async def create_child_select(form_data:api_schema.ChildSelCreate,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.create_childselect(db=db,form_data=form_data)
    return query


@api_router.get('/v1/child/sel/val',response_model=list[api_schema.GetChildSelVal])
async def filter_child_selval(id:Optional[int]=None,selval_id:Optional[int]=None,content :Optional[str]=None, value:Optional[str]=None,status:Optional[int]=None,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.filter_child_selval(db=db,content=content,value=value,selval_id=selval_id,status=status,id=id,)
    return query


@api_router.put('/v1/child/sel/value',response_model=api_schema.GetChildSelVal)
async def update_child_selval(form_data:api_schema.UpdateChildSelVal,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.update_child_selvalue(db=db,form_data=form_data)
    return query

@api_router.put('/v1/iiko/cakes',response_model=list[api_schema.GetCategory])
async def iiko_get_cakes(db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    key = authiiko()
    data = get_cakes(key)
    for i in data:
        if i['parent']==mastika:
            try:
                queries.create_cat(db=db,name=i['name'],price=i['defaultSalePrice'],iiko_id=i['id'])
            except:
                pass
    
    return queries.get_categories_iiko(db=db)



@api_router.get('/v1/category/full',response_model=api_schema.GetCategoryWithId)
async def get_category_with_id(id:int,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.get_category_withid(db=db,id=id)
    return query



@api_router.post('/v1/orders')
async def get_all_typeofdata(request:Request,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    form_data = await request.form()
    category_id = form_data['category_id']
    phone_number = form_data['phone_number']
    try:
        location = form_data['location']
    except:
        location = None
    try:
        branch = form_data['branch']
        branch_id = queries.get_dep_with_branch(db=db,id=branch).id
    except:
        branch_id=None

    order_cr = queries.create_order(db=db,category_id=category_id,user_id=request_user.id,phone_number=phone_number,location=location,department=branch_id)
    for field_name,field_value in form_data.items():
        
        if 'file' in field_name:
            generated_filename = generate_random_filename()+form_data[field_name].filename
            subcat_id = re.findall(r'\d+',field_name)[0]
            table_data = models.Value(subcat_id=subcat_id,order_id=order_cr.id,content=generated_filename)
            queries.create_value_order(db=db,table=table_data)
            with open('files/'+generated_filename, 'wb+') as f:
                shutil.copyfileobj(form_data[field_name].file,f)
        if 'selval' in field_name:
            field_id = re.findall(r'\d+',field_name)
            subcat_id = field_id[0]
            table_data = models.Value(subcat_id=subcat_id,order_id=order_cr.id,select_id=field_value)
            queries.create_value_order(db=db,table=table_data)
        if 'selval_child' in field_name:
            field_id = re.findall(r'\d+',field_name)
            subcat_id = field_id[0]
            table_data = models.Value(subcat_id=subcat_id,order_id=order_cr.id,selchild_id=field_value)
            queries.create_value_order(db=db,table=table_data)
        if 'sting' in field_name:
            field_id = re.findall(r'\d+',field_name)
            subcat_id = field_id[0]
            table_data = models.Value(subcat_id=subcat_id,order_id=order_cr.id,content=field_value)
            queries.create_value_order(db=db,table=table_data)

        if 'integer' in field_name:
            field_id = re.findall(r'\d+',field_name)
            subcat_id = field_id[0]
            table_data = models.Value(subcat_id=subcat_id,order_id=order_cr.id,content=field_value)
            queries.create_value_order(db=db,table=table_data)
    return {'success':True}


@api_router.get('/v1/orders',response_model=Union[api_schema.BaseOrder,list[api_schema.GetOrdervsId]])
async def get_one_order(id:Optional[int]=None,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    if id is not None:
        order_query = queries.get_order_with_id(db=db,id=id)
        value_query = queries.get_values_oforder(db=db,id=id)

        return {'order':order_query,'value':value_query}
    else:
        query = queries.getOrderList(db=db)
        return query




@api_router.put('/v1/iiko/departments',)
async def update_departments(db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    try:
        queries.insert_branches(db=db,items=list_departments(authiiko()))
    except:
        pass
    try:
        queries.insert_departments(db=db,
                                   items=list_stores(authiiko()))
    except:
        pass
    return {'success':True}


@api_router.get('/v1/departments',response_model=Page[api_schema.Branches_list])
async def get_branch_list(db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.get_branches_list(db=db)
    return paginate(query)













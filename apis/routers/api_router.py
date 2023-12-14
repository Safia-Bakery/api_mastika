from apis.schemas import api_schema
from fastapi import APIRouter,BackgroundTasks
from users.utils.user_micro import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from uuid import UUID
from apis.crud import queries
from datetime import datetime,date
from users.schemas.user_schema import User
from users.utils.user_micro import get_current_user
from typing import Optional,Union
from apis.utils.api_micro import authiiko,get_cakes,generate_random_filename,list_departments,list_stores,get_groups,sendtotelegram
from fastapi import Request,Form,UploadFile,File
import shutil
from fastapi_pagination import paginate,Page,add_pagination
import re
from typing import Annotated
from apis.models import models
import os
from dotenv import load_dotenv
load_dotenv()
BOTTOKEN = os.environ.get('BOT_TOKEN')

mastika  = ['30ed6a72-8771-4c81-91ad-e4b71305858d','d9dadbb0-8b97-4666-b740-fcfa47d11419','05b75ddf-3b87-4d1c-9483-5664f29d2c94','4c169130-114a-4314-989e-c48717ceb4e6','4b35d02b-af33-4175-ab84-c8beb646083b','bce298d5-e3aa-4b4c-b53f-322bdae63f59']
api_router = APIRouter()


@api_router.post('/v1/category')
async def create_category(name:Annotated[str,Form()],image:UploadFile = File(None),db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    if image:
        #for file in image:
        folder_name = f"files/{generate_random_filename()+image.filename}"
        with open(folder_name, "wb") as buffer:
            while True:
                chunk = await image.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        image=folder_name
    
    query = queries.create_cat(db=db,name=name,image=image)
    return {'success':True,'message':'this api currently inactive you data  will not be added to category list'}

@api_router.post('/v1/image/upload')
async def image_upload(image:list[UploadFile],db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    image_list = []
    for i in image:
            #for file in image:
        folder_name = f"files/{generate_random_filename()+i.filename}"
        image_list.append(folder_name)
        with open(folder_name, "wb") as buffer:
            while True:
                chunk = await i.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)

    return {'images':image_list}


@api_router.get('/v1/category',response_model=list[api_schema.GetCategory])
async def get_filter_category(name:Optional[str]=None,id:Optional[int]=None,status:Optional[int]=None,db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    query = queries.get_category(db=db,name=name,id=id,status=status)
    return query

@api_router.put('/v1/category',response_model=api_schema.GetCategory)
async def update_category(id:Annotated[int,Form()],name:Annotated[str,Form()]=None,status:Annotated[str,Form()]=None,image:UploadFile = File(None),db:Session=Depends(get_db),request_user: User = Depends(get_current_user)):
    if image is not None:
        #for file in image:
        folder_name = f"files/{generate_random_filename()+image.filename}"
        with open(folder_name, "wb") as buffer:
            while True:
                chunk = await image.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        image=folder_name
    query = queries.update_category(id=id,image=image,name=name,status=status,db=db)
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

@api_router.put('/v1/iiko/cakes')
async def iiko_get_cakes(background_task:BackgroundTasks,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    key = authiiko()
    groups = get_groups(key)
    def update_cakes():
        for i in groups:
            if i['id'] in mastika:
                try:
                    queries.add_product_groups(db=db,id=i['id'],code=i['code'],name=i['name'])
                except:
                    pass
        data = get_cakes(key)
        for i in data:
            if i['parent'] in mastika:
                try:
                
                    queries.add_products(db=db,name=i['name'],price=i['defaultSalePrice'],id=i['id'],groud_id=i['parent'],producttype=i['type'])
                except:
                    pass
    background_task.add_task(update_cakes)
    return {"success":True}

@api_router.put('/v1/cakes')
async def update_cake(form_data:api_schema.CakesUpdate,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.cake_update(db=db,form_data=form_data)
    return query





@api_router.get('/v1/category/full',response_model=api_schema.GetCategoryWithId)
async def get_category_with_id(id:int,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.get_category_withid(db=db,id=id)
    return query

"""
{
'1':{
    'floor':int
    }
}
"""

@api_router.post('/v1/orders',response_model=api_schema.GetOrdervsId)
async def get_all_typeofdata(form_data:api_schema.OrderCreation,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    #form_data = await request.form()
    #category_id = form_data['category_id']
    #phone_number = form_data['phone_number']
    #try:
    #    location = form_data['location']
    #except:
    #    location = None
    #try:
    #    branch = form_data['branch']
    #    branch_id = queries.get_dep_with_branch(db=db,id=branch).id
    #except:
    #    branch_id=None

    order_cr = queries.create_order(db=db,user_id=request_user.id,form_data=form_data)
    if order_cr:
        if form_data.filler is not None:
            for key,item in form_data.filler.items():
                query = queries.add_order_filling(db=db,order_id=order_cr.id,filling_id=item,floor=key)
    
    #for field_name,field_value in form_data.items():
    #    
    #    if 'file' in field_name:
    #        generated_filename = generate_random_filename()+form_data[field_name].filename
    #        subcat_id = re.findall(r'\d+',field_name)[0]
    #        table_data = models.Value(subcat_id=subcat_id,order_id=order_cr.id,content=generated_filename)
    #        queries.create_value_order(db=db,table=table_data)
    #        with open('files/'+generated_filename, 'wb+') as f:
    #            shutil.copyfileobj(form_data[field_name].file,f)
    #    if 'selval' in field_name:
    #        field_id = re.findall(r'\d+',field_name)
    #        subcat_id = field_id[0]
    #        table_data = models.Value(subcat_id=subcat_id,order_id=order_cr.id,select_id=field_value)
    #        queries.create_value_order(db=db,table=table_data)
    #    if 'selval_child' in field_name:
    #        field_id = re.findall(r'\d+',field_name)
    #        subcat_id = field_id[0]
    #        table_data = models.Value(subcat_id=subcat_id,order_id=order_cr.id,selchild_id=field_value)
    #        queries.create_value_order(db=db,table=table_data)
    #    if 'sting' in field_name:
    #        field_id = re.findall(r'\d+',field_name)
    #        subcat_id = field_id[0]
    #        table_data = models.Value(subcat_id=subcat_id,order_id=order_cr.id,content=field_value)
    #        queries.create_value_order(db=db,table=table_data)
    #    if 'integer' in field_name:
    #        field_id = re.findall(r'\d+',field_name)
    #        subcat_id = field_id[0]
    #        table_data = models.Value(subcat_id=subcat_id,order_id=order_cr.id,content=field_value)
    #        queries.create_value_order(db=db,table=table_data)
    return order_cr

@api_router.post('/v1/orders/dynamic')
async def getdynamic_values(request:Request,db:Session=Depends(get_db)):#,request_user:User=Depends(get_current_user)):
    form_data = await request.form()
    order_id = form_data['order_id']
    for field_name,field_value in form_data.items():
        #tr
            if 'child' in field_name:
                field_id = re.findall(r'\d+',field_name)
                subcat_id = field_id[0]
                subcategory = queries.get_subcategory_with_id(db=db,id=subcat_id)
                if subcategory:
                    table_data = models.Value(subcat_id=subcat_id,order_id=order_id,selchild_id=field_value)
                    queries.create_value_order(db=db,table=table_data)
            else:
                if field_name !='order_id':
                    subcat_id = int(field_name)
                    subcategory = queries.get_subcategory_with_id(db=db,id=subcat_id)
                    if subcategory.contenttype_id ==1:
                        table_data = models.Value(subcat_id=subcat_id,order_id=order_id,content=field_value)
                        queries.create_value_order(db=db,table=table_data)
                    if subcategory.contenttype_id==2:
                        generated_filename = generate_random_filename()+form_data[field_name].filename
                        table_data = models.Value(subcat_id=subcat_id,order_id=order_id,content=generated_filename)
                        queries.create_value_order(db=db,table=table_data)
                        with open('files/'+generated_filename, 'wb+') as f:
                            shutil.copyfileobj(form_data[field_name].file,f)
                    if subcategory.contenttype_id ==3:
                        table_data = models.Value(subcat_id=subcat_id,order_id=order_id,content=field_value)
                        queries.create_value_order(db=db,table=table_data)
                    if subcategory.contenttype_id==4:
                        table_data = models.Value(subcat_id=subcat_id,order_id=order_id,select_id=field_value)
                        queries.create_value_order(db=db,table=table_data)
        #except:
        #    pass
    return {'success':True}

is_delivery = ["Доставка","Самовывоз"]

@api_router.put('/v1/orders')
async def update_order(form_data:api_schema.OrderUpdate,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.update_order(db=db,form_data=form_data)
    if query:

        if form_data.filler is not None:
            queries.delete_order_filling(db=db,order_id=query.id)
            for key,item in form_data.filler.items():
                queries.add_order_filling(db=db,order_id=query.id,filling_id=item,floor=key)
    if form_data.status==1:
        is_delivery = ["Доставка","Самовывоз"]
        if query.is_delivery==1:

            address = f"Aдрес: {query.address}"

        else: 
            address = f"Филиал: {query.order_br.branch_dr.name}"
        nachin_text = f""
        for i in range(len(query.order_fill)):
            nachin_text+f"Начинка {i+1} этаж: {query.order_fill[i].filler.name}\n"
        palitra_text = f""
        for i in dict(query.color_details).keys():
            palitra_text+f"Палитра {i} этаж: {query.color_details[i]}"
        order_product = f""
        for i in query.product_order:
            order_product+f"{i.product_r.name}: {i.name}\n"
        
        packaging = [None,'Бесплатная упаковка','платная упаковка']
        timestamp = datetime.strptime(query.deliver_date, '%Y-%m-%d %H:%M:%S.%f%z')
        message  = f"""
        Заказ: #{query.id}s\n\
        Тип заказа🏃: {is_delivery[query.is_delivery]}\n\
        {address}\n\n\
        Направление: {query.order_vs_category.name}\n\
        Количество порций: {query.portion}\n\
        Этаж: {len(query.order_fill)}\n\
        {nachin_text}\
        {palitra_text}\
        Упаковка: {packaging[query.packaging]}\n\
        {order_product}\n\
        Комментарий: {query.comment}\n\n\
        Поставка: #{timestamp.day}{timestamp.month}{timestamp.year}s
        """
        sendtotelegram(bot_token=BOTTOKEN,chat_id=6083044524,message_text=message)
        
    return query



@api_router.post('/v1/orders/products')
async def product_add(form_data:list[api_schema.OrderProducts],db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    for i in form_data:
        query =queries.create_order_products(db=db,form_data=i)
    return {'success':True}


@api_router.get('/v1/orders',response_model=api_schema.BaseOrder)
async def get_one_order(id:int,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    if id is not None:
        order_query = queries.get_order_with_id(db=db,id=id)
        value_query = queries.get_values_oforder(db=db,id=id)

        return {'order':order_query,'value':value_query}
    else:
        query = queries.getOrderList(db=db)
        return {'order':query}

@api_router.get('/v1/orders/all',response_model=Page[api_schema.GetOrdervsId])
async def get_one_order(status:Optional[int]=None,cake:Optional[UUID]=None,is_delivery:Optional[int]=None,created_at:Optional[date]=None,branch_id:Optional[UUID]=None,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    
    query = queries.getOrderList(db=db,status=status,cake=cake,is_delivery=is_delivery,created_at=created_at,branch_id=branch_id)
    return paginate(query)


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
async def get_branch_list(id:Optional[UUID]=None,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.get_branches_list(db=db,id=id)
    return paginate(query)


@api_router.get('/v1/products/groups',response_model=list[api_schema.GroupsGet])
async def get_group_list(db:Session=Depends(get_db),id:Optional[UUID]=None,name:Optional[str]=None,request_user:User=Depends(get_current_user)):
    query = queries.get_product_groups(db=db,id=id,name=name)
    return query

@api_router.get('/v1/products',response_model=list[api_schema.ProductsFilter])
async def get_product_list(db:Session=Depends(get_db),id:Optional[UUID]=None,group_id:Optional[UUID]=None,name:Optional[str]=None,status:Optional[int]=None,request_user:User=Depends(get_current_user)):
    query = queries.get_products(db=db,id=id,name=name,group_id=group_id,status=status)
    return query


@api_router.put('/v1/products')
async def update_product(form_data:api_schema.OrderProductUpdate,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.update_order_product(db=db,form_data=form_data)
    return {'success':True}


@api_router.post('/v1/fillings',response_model=api_schema.FillingGet)
async def add_fillings(form_data:api_schema.FillingAddGet,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.add_filling(db=db,form_data=form_data)
    return query

@api_router.put('/v1/fillings',response_model=api_schema.FillingGet)
async def update_filling(form_data:api_schema.FillingUpdate,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.update_filling(db=db,form_data=form_data)
    return query

@api_router.get('/v1/fillings',response_model=list[api_schema.FillingGet])
async def filter_fillings(id:Optional[int]=None,name:Optional[str]=None,ptype:Optional[int]=None,status:Optional[int]=None,category_id:Optional[int]=None,db:Session=Depends(get_db),request_user:User=Depends(get_current_user)):
    query = queries.get_filling(db=db,id=id,ptype=ptype,name=name,status=status,category_id=category_id)
    return query











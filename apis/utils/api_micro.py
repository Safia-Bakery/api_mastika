from dotenv import load_dotenv
import os 
import random
import string
load_dotenv()
import requests
import xml.etree.ElementTree as ET

LOGIN_IIKO = os.environ.get('LOGIN_IIKO')
PASSWORD_IIKO = os.environ.get('PASSWORD_IIKO')
BASE_URL = os.environ.get('BASE_URL')
IIKO_CLOUD_API_KEY = os.environ.get('IIKO_CLOUD_API_KEY')
IIKO_CLOUD_API_URL = os.environ.get('IIKO_CLOUD_API_URL')




def authiiko():
    data  = requests.get(f"{BASE_URL}/resto/api/auth?login={LOGIN_IIKO}&pass={PASSWORD_IIKO}")
    key = data.text
    return key


def authiikocloud():
    data  = requests.post(f"{IIKO_CLOUD_API_URL}/api/1/access_token",json={"apiLogin":IIKO_CLOUD_API_KEY})
    key = data.json()['token']

    return key


def iikocloud_departments(key):
    data = requests.get(f"{IIKO_CLOUD_API_URL}/api/1/organizations",headers={"Authorization":"Bearer "+key}).json()

    return data

def iikocloud_terminals(key,org_id):
    data = requests.post(f"{IIKO_CLOUD_API_URL}/api/1/terminal_groups",headers={"Authorization":"Bearer "+key},json={"organizationIds":[org_id]})
    return data.json()



def iikocloud_payment_types(key,org_id):
    data = requests.post(f"{IIKO_CLOUD_API_URL}/api/1/payment_types",headers={"Authorization":"Bearer "+key},json={"organizationIds":[org_id]})
    return data.json()


def iikocloud_order_types(key,org_id):
    data = requests.post(f"{IIKO_CLOUD_API_URL}/api/1/deliveries/order_types",headers={"Authorization":"Bearer "+key},json={"organizationIds":[org_id]})
    return data.json()



def get_groups(key): 
    groups = requests.get(f"{BASE_URL}/resto/api/v2/entities/products/group/list?key={key}").json()
    return groups

def get_cakes(key):
    products = requests.get(f"{BASE_URL}/resto/api/v2/entities/products/list?key={key}&includeDeleted=false").json()
    return products



def generate_random_filename(length=30):
    characters = string.ascii_letters + string.digits
    random_filename = ''.join(random.choice(characters) for _ in range(length))
    return random_filename



def list_departments(key):
    departments = requests.get(f"{BASE_URL}/resto/api/corporation/departments?key={key}")
    root = ET.fromstring(departments.content)
    corporate_item_dtos = root.findall('corporateItemDto')
    names = [[item.find('name').text, item.find('id').text] for item in corporate_item_dtos]
    return names



def list_stores(key):
    departments = requests.get(f"{BASE_URL}/resto/api/corporation/stores?key={key}")
    root = ET.fromstring(departments.content)
    corporate_item_dtos = root.findall('corporateItemDto')

    names = [[item.find('name').text, item.find('id').text,item.find('parentId').text] for item in corporate_item_dtos]
    return names



def sendtotelegram(bot_token,chat_id,message_text,files):
    

    # Create the request payload
    payload = {
        'chat_id': chat_id,
        'caption': message_text,
        #'reply_markup': keyboard,
        #'parse_mode': 'MARKDOWN'
    }

    # Send the request to send the inline keyboard message
    response = requests.post(f'https://api.telegram.org/bot{bot_token}/sendPhoto', data=payload,files=files)
    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False
    
def sendtotelegramwithoutimage(bot_token,chat_id,message_text):
    

    # Create the request payload
    payload = {
        'chat_id': chat_id,
        'text': message_text,
        #'reply_markup': keyboard,
        #'parse_mode': 'MARKDOWN'
    }

    # Send the request to send the inline keyboard message
    response = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', json=payload)
    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False
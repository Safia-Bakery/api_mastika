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


def authiiko():
    data  = requests.get(f"{BASE_URL}/resto/api/auth?login={LOGIN_IIKO}&pass={PASSWORD_IIKO}")

    key = data.text
    return key


def get_groups(key): 
    groups = requests.get(f"{BASE_URL}/resto/api/v2/entities/products/group/list?key={key}").json()
    return groups

def get_cakes(key):
    products = requests.get(f"{BASE_URL}/resto/api/v2/entities/products/list?key={key}&includeDeleted=false").json()
    return products



def generate_random_filename(length=30):
    # Define the characters you want to use in the random filename
    characters = string.ascii_letters + string.digits

    # Generate a random filename of the specified length
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


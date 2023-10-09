from dotenv import load_dotenv
import os 
import random
import string
load_dotenv()
import requests

LOGIN_IIKO = os.environ.get('LOGIN_IIKO')
PASSWORD_IIKO = os.environ.get('PASSWORD_IIKO')
BASE_URL = os.environ.get('BASE_URL')


def authiiko():
    data  = requests.get(f"{BASE_URL}/resto/api/auth?login={LOGIN_IIKO}&pass={PASSWORD_IIKO}")

    key = data.text
    return key

def get_cakes(key):
    products = requests.get(f"{BASE_URL}/resto/api/v2/entities/products/list?key={key}&includeDeleted=false").json()
    return products



def generate_random_filename(length=30):
    # Define the characters you want to use in the random filename
    characters = string.ascii_letters + string.digits

    # Generate a random filename of the specified length
    random_filename = ''.join(random.choice(characters) for _ in range(length))

    return random_filename
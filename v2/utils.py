from passlib.context import CryptContext
import re
import datetime
import time
import base64
import jalali_date
from settings import BASE_DIR


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str):
    return pwd_context.hash(password)


def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def save_image(image):
    pattern = r'.*\/(\w+);.*'
    image_data = image.split(',')
    image_type = image_data[0]
    image_type = re.search(pattern, image_type).group(1)
    base64_image = image_data[1]
    base64_image_to_byte = base64_image.encode('utf-8')
    image_name = jalali_date.Gregorian(datetime.datetime.now().date()).persian_string("{}_{}_{}")
    image_url = f'/statics/images/upload/post/{image_name}_{time.time()}.{image_type}'

    with open(f'{BASE_DIR}{image_url}', 'wb') as file:
        decoded_base64_image = base64.decodebytes(base64_image_to_byte)
        file.write(decoded_base64_image)

    return image_url
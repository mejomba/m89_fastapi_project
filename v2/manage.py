import argparse
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import utils


POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'secretpassword'
POSTGRES_DB = 'postgres'
DB_HOST = 'fastapi_db'

# DATABASE_URL = "postgresql://hhcxbbfm:sZV-t7aFHw-KW3eRuFMkg-6gLp1KxfJh@mouse.db.elephantsql.com/hhcxbbfm"
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:5432/{POSTGRES_DB}"  # databasename://user:password@ip_address/database

while True:
    try:
        conn = psycopg2.connect(host=DB_HOST, database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                                cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print('connect to database.')
        break
    except Exception as err:
        print('connect to database fail')
        print(err)
        time.sleep(2)


parser = argparse.ArgumentParser()
parser.add_argument('--createsuperuser', help="create super user and store")

args = parser.parse_args()

if args:
    username = args.createsuperuser
    email = input('email: ')
    password = input('password: ')
    first_name = input('first_name: ')
    last_name = input('last_name: ')
    image = '/statics/images/upload/user/no_image.png'
    role = 'admin'

    if username and email and password and first_name and last_name and role:
        password = utils.hash_password(password)
        query = """INSERT INTO users (email, username, first_name, last_name, password, image, role) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING *"""
        data = email, username, first_name, last_name, password, image, role
        try:
            cur.execute(query, data)
            conn.commit()
            print(f'create superuser done.')
        except Exception as e:
            print(e)
    else:
        print('\nall input required\n')

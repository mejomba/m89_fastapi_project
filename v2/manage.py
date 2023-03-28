import argparse
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import utils

DATABASE_URL = "postgresql://hhcxbbfm:sZV-t7aFHw-KW3eRuFMkg-6gLp1KxfJh@mouse.db.elephantsql.com/hhcxbbfm"

while True:
    try:
        conn = psycopg2.connect(host='mouse.db.elephantsql.com', database='hhcxbbfm', user='hhcxbbfm', password='sZV-t7aFHw-KW3eRuFMkg-6gLp1KxfJh',
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
    role = 'admin'

    if username and email and password and first_name and last_name and role:
        password = utils.hash_password(password)
        query = """INSERT INTO users (email, username, first_name, last_name, password, role) VALUES (%s,%s,%s,%s,%s,%s) RETURNING *"""
        data = email, username, first_name, last_name, password, role
        try:
            cur.execute(query, data)
            conn.commit()
            print(f'create superuser done.')
        except Exception as e:
            print(e)
    else:
        print('\nall input required\n')

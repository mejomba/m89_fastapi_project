from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

POSTGRES_USER = 'm89_fastapi_user'
POSTGRES_PASSWORD = 'secretpassword'
POSTGRES_DB = 'm89_fastapi_blog'
DB_HOST = 'fastapi_db'
# DATABASE_URL = "postgresql://postgres:1@localhost:5432/fastapi_project2"  # databasename://user:password@ip_address/database
# DATABASE_URL = "postgresql://hhcxbbfm:sZV-t7aFHw-KW3eRuFMkg-6gLp1KxfJh@mouse.db.elephantsql.com/hhcxbbfm"  # databasename://user:password@ip_address/database
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:5432/{POSTGRES_DB}"  # databasename://user:password@ip_address/database
engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BASE = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
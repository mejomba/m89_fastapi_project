from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:1@localhost/fastapi_project"  # databasename://user:password@ip_address/database
engin = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(bind=engin, autocomit=False, autoflush=False)
BASE = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
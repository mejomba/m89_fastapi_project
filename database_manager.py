from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:1@localhost:5432/fastapi_project"  # databasename://user:password@ip_address/database
engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(autocomit=False, autoflush=False, bind=engine)
BASE = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
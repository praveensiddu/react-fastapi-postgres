from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


if os.getenv("DATABASE_URL") == None:
    print("Environment variable DATABASE_URL must be set")
    print("example postgresql://fastapi_user:fastapi_pass@localhost/fastapi_db")
    exit(-1)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

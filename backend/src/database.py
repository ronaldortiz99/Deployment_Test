import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .utils import settings
if settings.production:
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./services/backend/data.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} )
#check_same_thread...is needed only for SQLite. It's not needed for other databases.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
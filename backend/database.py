from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config
import os

Base = declarative_base()
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    from models import User, OTP, RefreshToken
    Base.metadata.create_all(bind=engine)
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

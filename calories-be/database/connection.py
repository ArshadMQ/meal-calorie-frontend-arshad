from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database.config import cfg

DATABASE_URL = cfg("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def db_session_connection():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


def check_db_connection():
    try:
        with engine.connect() as connection:
            connection.scalar(text("SELECT 1"))
            return True
    except Exception as e:
        return False

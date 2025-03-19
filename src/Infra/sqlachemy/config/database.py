from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_FILE_NAME = "database.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{SQLALCHEMY_FILE_NAME}"

CONNECT_ARGS = {"check_same_thread": False}
engine = create_engine(SQLALCHEMY_DATABASE_URL , connect_args=CONNECT_ARGS)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_session_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close
from sqlalchemy.orm import sessionmaker, declarative_base 
from sqlalchemy import create_engine  



DATABASE_URL = "sqlite:///./data.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()


SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db 
    finally:
        db.close()


        
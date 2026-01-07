from sqlalchemy import Column, String, Integer
from database import Base, engine 



class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)
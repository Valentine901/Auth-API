from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session 
from models import User
from database import get_db 


SECRET_KEY = "HFY38WLIG39NFKLRO384BDE38393BGDW48N3I22DKSDE994"
ALGORITHM = "HS256"
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/user/")

password_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    return password_context.hash(password)

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    now = datetime.utcnow()

    expire = now + timedelta(minutes=30)
    to_encode.update({"exp": expire})

    jwt_encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_encoded

def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db) ):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except JWTError:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user
    
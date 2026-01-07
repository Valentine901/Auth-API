from sqlalchemy.orm import Session 
from database import get_db
from schemas import CreateUser, UserResponse, LoginUser, TokenResponse
from auth import create_access_token, verify_password, hash_password, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, Depends, APIRouter
from models import User

router = APIRouter(prefix="/user")


@router.post("/register", response_model=UserResponse)
def register(data: CreateUser, db: Session = Depends(get_db)):

    user = db.query(User).filter((User.username == data.username) | (User.email == data.email)).first()

    if user:
        raise HTTPException(status_code=400, detail="User already existed")
    
    hash = hash_password(data.password)

    new_user = User(username=data.username, email=data.email, password=hash)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 


# @router.post("/", response_model=TokenResponse)
# def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

#     user = db.query(User).filter(User.username == data.username).first()
#     if not user:
#         raise HTTPException(status_code=401, detail="Unauthorized User")
    
#     verified_password = verify_password(data.password, user.password)
#     if not verified_password:
#         raise HTTPException(status_code=401, detail="Unauthorized User")
#     access_token = create_access_token({"sub": str(user.id)})

#     return {"access_token":access_token, "token_type":"bearer"}
    


@router.post("/", response_model=TokenResponse)
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.username == data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized User")
    
    verified_password = verify_password(data.password, user.password)
    if not verified_password:
        raise HTTPException(status_code=401, detail="Unauthorized User")

    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type":"bearer"}    

@router.get("/users", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):

    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail='No user found')
    return users

@router.get("/")
def get_message( db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    user = db.query(User).filter(User.id == current_user.id ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Unauthoirzed User")
    return {"message":"You are now Authorized!"}
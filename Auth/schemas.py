from pydantic import BaseModel 
from typing import Optional

class CreateUser(BaseModel):
    username: str 
    email: str 
    password: str 

class UserResponse(BaseModel):
    id: int 
    username: str 
    email: str 


class TokenResponse(BaseModel):
    access_token: str 
    token_type: Optional[str] = "bearer"

class LoginUser(BaseModel):
    email: str 
    password: str 

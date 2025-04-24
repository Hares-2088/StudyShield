# auth/models.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str  # Plain text password from registration

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
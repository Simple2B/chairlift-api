from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: Optional[str]
    picture: Optional[str]
    google_openid_key: Optional[str]
    apple_openid_key: Optional[str]

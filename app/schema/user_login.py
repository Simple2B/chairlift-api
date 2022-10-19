from typing import Optional
from pydantic import BaseModel


class UserLogin(BaseModel):
    user_id: str
    password: str


class UserGoogleLogin(BaseModel):
    email: str
    username: str
    google_openid_key: str
    picture: Optional[str]

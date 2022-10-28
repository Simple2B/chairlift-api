from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


from app.model import Role


class UserOut(BaseModel):
    username: str
    email: EmailStr
    picture: Optional[str]
    is_deleted: bool
    created_at: datetime
    role: Role

    class Config:
        orm_mode = True


class GooglKeys(BaseModel):
    google_client_id: str
    google_api_key: str


class StripeKey(BaseModel):
    stripe_public_key: str

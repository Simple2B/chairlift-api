from pydantic import BaseModel


class ResetPasswordData(BaseModel):
    verification_token: str
    password: str

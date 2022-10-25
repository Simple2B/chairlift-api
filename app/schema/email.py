from typing import List

from pydantic import EmailStr, BaseModel


class EmailListSchema(BaseModel):
    """
    Scheme for checking an email in the functionality responsible for sending an email

    """

    email: List[EmailStr]


class EmailSchema(BaseModel):
    email: EmailStr

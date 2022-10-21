from typing import List

from pydantic import EmailStr, BaseModel


class EmailSchema(BaseModel):
    """
    Scheme for checking an email in the functionality responsible for sending an email

    """

    email: List[EmailStr]

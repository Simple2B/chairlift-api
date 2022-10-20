from typing import List

from pydantic import EmailStr, BaseModel


class EmailSchema(BaseModel):
    email: List[EmailStr]

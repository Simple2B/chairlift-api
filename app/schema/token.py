from pydantic import BaseModel

import app.schema as s


class Token(BaseModel):
    access_token: str
    token_type: str
    user: s.UserOut


class TokenData(BaseModel):
    id: int

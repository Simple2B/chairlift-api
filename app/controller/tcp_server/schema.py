from pydantic import BaseModel


class ServerConfig(BaseModel):
    PORT: int

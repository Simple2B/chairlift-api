import enum
from datetime import datetime


class Role(enum.Enum):
    Admin = "Admin"
    Owner = "Owner"
    Client = "Client"
    NoneUser = "None"

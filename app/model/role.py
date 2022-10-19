import enum


class Role(enum.Enum):
    Admin = "Admin"
    Owner = "Owner"
    Client = "Client"
    NoneRole = "None"

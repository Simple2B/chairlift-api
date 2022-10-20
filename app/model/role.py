import enum

# TODO PERMISSIONS AND ROLES


class Role(enum.Enum):
    """
    Enumeration class for roles

    Args:

        (Admin): Admin Role
        (Owner): Owner Role
        (Client): Client Role
        (NoneRole): Role for uknown user

    """

    Admin = "Admin"
    Owner = "Owner"
    User = "User"

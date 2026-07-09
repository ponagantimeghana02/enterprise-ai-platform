roles = {

    "admin": [
        "read",
        "write",
        "delete"
    ],

    "manager": [
        "read",
        "write"
    ],

    "employee": [
        "read"
    ]

}


def check_permission(role, permission):

    return permission in roles.get(
        role,
        []
    )
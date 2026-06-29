from core.response import success


def whoami(user):
    return success(
        "User information",
        {
            "id": user["id"],
            "name": user["name"],
            "username": user["username"],
        },
    )

from core.command_router import execute

user = {
    "id": 6123502479,
    "name": "MD. RADOAN",
    "username": "mdradoan6608",
}

print(execute("connection", user=user))

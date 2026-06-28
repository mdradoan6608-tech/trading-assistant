AUTHORIZED_USERS = set()


def add_user(user_id: int):
    AUTHORIZED_USERS.add(user_id)


def remove_user(user_id: int):
    AUTHORIZED_USERS.discard(user_id)


def is_authorized(user_id: int) -> bool:
    return user_id in AUTHORIZED_USERS

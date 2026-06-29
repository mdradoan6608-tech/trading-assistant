AUTHORIZED_USERS = {
    6123502479,
}


def is_authorized(user_id):
    return user_id in AUTHORIZED_USERS

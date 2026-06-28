from core.auth import add_user, is_authorized

USER_ID = 123456789

print(is_authorized(USER_ID))

add_user(USER_ID)

print(is_authorized(USER_ID))

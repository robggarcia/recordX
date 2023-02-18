from db.mongodb import get_user_collection

users_col = get_user_collection()


def get_all_users():
    return users_col


def login_user(username, password):
    return users_col


def register_user(username, email, password):
    return users_col


def update_user(id, data):
    return users_col


def send_message(id, user, message):
    return users_col

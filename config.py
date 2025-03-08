import os


def get_email() -> str:
    email = os.getenv("EMAIL")
    if email is None:
        raise Exception("Email is not set in ENV")
    return email


def get_password() -> str:
    password = os.getenv("password")
    if password is None:
        raise Exception("Password is not set in ENV")
    return password


def get_login_url() -> str:
    url = os.getenv("LOGIN_URL")
    if url is None:
        raise Exception("Login URL is not set in ENV")
    return url


def get_profile_url() -> str:
    url = os.getenv("PROFILE_URL")
    if url is None:
        raise Exception("Profile URL is not set in ENV")
    return url


def get_wishlist_url() -> str:
    url = os.getenv("WISHLIST")
    if url is None:
        raise Exception("Wishlist URL is not set in ENV")
    return url


def get_db_url() -> str:
    url = os.getenv("DB_URL")
    if url is None:
        raise Exception("DB URL is not set in ENV")
    return url

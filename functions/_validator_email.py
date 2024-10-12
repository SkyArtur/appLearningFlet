from re import search


def validate_email(email: str):
    try:
        valid_email = search(r'^([a-z0-9_]{5,100})@([a-z0-9]{5,100}).([a-z]{2,3})(.)?([a-z]{2})?$', email).string
        return valid_email
    except (TypeError, ValueError, AttributeError):
        return False


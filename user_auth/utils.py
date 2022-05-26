from django.contrib.auth import authenticate


def validate_user_password(username, password):
    user = None
    try:
        user = authenticate(username=username, password=password)
    except Exception:
        pass
    return user

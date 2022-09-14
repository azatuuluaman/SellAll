from django.contrib.auth import authenticate, get_user_model

from decouple import config

User = get_user_model()


def login_social_user(email) -> dict:
    filtered_user_by_email = User.objects.filter(email=email)

    if not filtered_user_by_email.exists():
        return {}

    login_user = authenticate(email=email, password=config('SOCIAL_SECRET'))
    return login_user.tokens()


def register_user_by_social(email, first_name, last_name) -> dict:
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():
        return {}

    user = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'password': config('SOCIAL_SECRET')
    }

    user = User.objects.create_user(**user)
    user.is_active = True
    user.save()

    new_user = authenticate(email=email, password=config('SOCIAL_SECRET'))

    return new_user.tokens()

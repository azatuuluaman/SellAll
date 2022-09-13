from django.contrib.auth import authenticate, get_user_model

from decouple import config

User = get_user_model()


def login_social_user(provider, email) -> dict:
    filtered_user_by_email = User.objects.filter(email=email)

    if not filtered_user_by_email.exists():
        return register_user_by_social(provider, email)

    # if provider != filtered_user_by_email[0].social_auth:
    #     filtered_user_by_email[0].social_auth += provider

    login_user = authenticate(email=email, password=config('SOCIAL_SECRET'))
    return {'auth_token': login_user.tokens()}


def register_user_by_social(provider, email) -> dict:
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():
        return {}

    user = {
        'email': email,
        'password': config('SOCIAL_SECRET')
    }

    user = User.objects.create_user(**user)
    user.is_active = True
    user.social_auth = provider
    user.save()

    new_user = authenticate(email=email, password=config('SOCIAL_SECRET'))

    return {'auth_token': new_user.tokens()}

from django.contrib.auth import authenticate, get_user_model

from decouple import config

User = get_user_model()


def login_google_user(user_data) -> dict:
    email = user_data.get('email')

    filtered_user_by_email = User.objects.filter(email=email)

    if not filtered_user_by_email.exists():
        return register_user_by_google(user_data)

    login_user = authenticate(email=email, password=config('SOCIAL_SECRET'))
    return login_user.tokens()


def register_user_by_google(user_data) -> dict:
    email = user_data.get('email')
    first_name = user_data.get('given_name')
    last_name = user_data.get('family_name')

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

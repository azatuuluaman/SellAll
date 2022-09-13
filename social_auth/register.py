from django.contrib.auth import authenticate, get_user_model

from rest_framework.exceptions import AuthenticationFailed

from decouple import config

User = get_user_model()


def register_social_user(provider, email):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].social_auth:

            registered_user = authenticate(
                email=email, password=config('SOCIAL_SECRET'))

            return {
                'email': registered_user.email,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].social_auth)

    else:
        user = {
            'email': email,
            'password': config('SOCIAL_SECRET')}

        user = User.objects.create_user(**user)
        user.is_active = True
        user.social_auth = provider
        user.save()

        new_user = authenticate(
            email=email, password=config('SOCIAL_SECRET'))
        return {
            'email': new_user.email,
            'tokens': new_user.tokens()
        }

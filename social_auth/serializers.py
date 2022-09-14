from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from decouple import config

from .google import Google
from .facebook import Facebook
from .auth import login_social_user, register_user_by_social


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Facebook.validate(auth_token)

        email = user_data.get('email')
        first_name = user_data.get('given_name')
        last_name = user_data.get('family_name')

        auth = login_social_user(email=email)

        if not auth:
            auth = register_user_by_social(email, first_name, last_name)

        return auth


class GoogleSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of google related data"""
    auth_token = serializers.JSONField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)

        if not user_data.get('sub'):
            raise serializers.ValidationError('The token is invalid or expired. Please login again.')

        if user_data.get('aud') != config('GOOGLE_CLIENT_ID'):
            raise AuthenticationFailed('oops, who are you?')

        email_verified = user_data.get('email_verified')

        if not email_verified:
            raise serializers.ValidationError('Email not verified!')

        email = user_data.get('email')
        first_name = user_data.get('given_name')
        last_name = user_data.get('family_name')

        auth = login_social_user(email=email)

        if not auth:
            auth = register_user_by_social(email, first_name, last_name)

        return auth

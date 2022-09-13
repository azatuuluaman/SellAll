from django.conf import settings
from rest_framework import serializers
from decouple import config
from . import google, facebook
from .register import register_social_user
from rest_framework.exceptions import AuthenticationFailed


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
            email = user_data['email']
            provider = settings.FACEBOOK
            return register_social_user(
                provider=provider,
                email=email,
            )
        except Exception as identifier:

            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )


class GoogleSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of google related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != config('GOOGLE_CLIENT_ID'):
            raise AuthenticationFailed('oops, who are you?')

        email = user_data['email']
        provider = settings.GOOGLE

        return register_social_user(
            provider=provider, email=email)

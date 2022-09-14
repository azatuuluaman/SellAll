from django.conf import settings
from rest_framework import serializers
from decouple import config
from . import google, facebook
from .auth import login_google_user
from rest_framework.exceptions import AuthenticationFailed


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
            email = user_data['email']

            result = login_google_user(email=email)

            if not result:
                return serializers.ValidationError("User already use another social")

            return result

        except Exception as identifier:

            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )


class GoogleSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of google related data"""
    auth_token = serializers.JSONField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)

        if not user_data.get('sub'):
            raise serializers.ValidationError('The token is invalid or expired. Please login again.')

        if user_data.get('aud') != config('GOOGLE_CLIENT_ID'):
            raise AuthenticationFailed('oops, who are you?')

        email_verified = user_data.get('email_verified')

        if not email_verified:
            raise serializers.ValidationError('Email not verified!')

        result = login_google_user(user_data=user_data)

        if not result:
            raise serializers.ValidationError("User already use another social!")

        return result

import random

from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation

from rest_framework import serializers
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from advertisement.utils import Redis

from .models import User
from .tasks import send_activation_mail

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email уже используется')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        activation_code = random.randint(1000, 9999)

        redis = Redis()
        key = f'activate_code_{activation_code}'
        redis.conn.set(key, user.pk)
        redis.conn.expire(key, 3600)
        redis.close()

        send_activation_mail.delay(user.email, activation_code)
        return user

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'password', 'password_confirm']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'phone_number',
            'first_name',
            'last_name',
        )


class UserUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_null=True)
    last_name = serializers.CharField(required=False, allow_null=True)
    email = serializers.CharField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_null=True)
    password = serializers.CharField(required=False, allow_null=True)
    password_confirm = serializers.CharField(required=False, allow_null=True)

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('password_confirm')

        if password:
            if not confirm_password:
                raise serializers.ValidationError({'password_confirm': 'Can\'t be empty, if password field exists!'})

            if password != confirm_password:
                raise serializers.ValidationError({'password_confirm': 'Passwords don\'t match!'})

            del data['password_confirm']
        else:
            if confirm_password:
                raise serializers.ValidationError({'password': 'Can\'t be empty, if password_confirm field exists!'})

        return data

    def update(self, user, data):
        validated_data = self.validate(data)

        password = validated_data.get('password')

        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')

        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        if email:
            user.email = email

        if phone_number:
            user.phone_number = phone_number

        if password:
            old_token = user.tokens().get('refresah')
            token = RefreshToken(old_token)
            token.blacklist()

            user.set_password(password)
            del validated_data['password']

        user.save()
        return user

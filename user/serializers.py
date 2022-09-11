import random

from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation

from rest_framework import serializers

from advertisement.utils import Redis
from .models import User
from .utils import send_activation_mail

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
        send_activation_mail(user.email, activation_code)
        return user

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'password', 'password_confirm']

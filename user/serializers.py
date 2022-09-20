import random

from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation

from rest_framework import serializers

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

    def update(self, instance, data):
        validated_data = self.validate(data)

        instance = User.objects.filter(pk=instance.pk)
        user = instance[0]
        password = validated_data.get('password')

        if password:
            user.set_password(password)
            del validated_data['password']

        instance.update(**validated_data)

        user.save()

        return user

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from advertisement.utils import Redis

User = get_user_model()

URL = 'http://localhost:8000/'


class UserTestCase(APITestCase):
    model = User
    email = 'admin@gmail.com'
    password = 'admin12345'
    activate_code = 1234
    key = f'activate_code_{activate_code}'

    def register_user(self, data):
        response = self.client.post(reverse('register'), data=data)
        return response

    def create_user(self, data):
        user = User.objects.create_user(**data)
        return user

    def get_user(self, email):
        user = User.objects.get(email=email)
        return user

    def activate_user(self, data, user):
        response = self.client.post(reverse('activate'), data=data)

        if response.status_code == status.HTTP_200_OK:
            user.is_active = True
            user.save()

        return response

    def create_activate_code(self, redis, key, user_pk):
        redis.set(key, user_pk)

    def get_redis_conn(self):
        redis = Redis()
        return redis.conn

    def test_register(self):
        user_register_data = {
            'email': self.email,
            'first_name': 'Admin',
            'last_name': 'Gmail',
            'phone_number': '+996505117733',
            'password': self.password,
            'password_confirm': self.password
        }

        response = self.register_user(user_register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_activate(self):
        key = self.key

        data = {
            'email': self.email,
            'password': self.password
        }

        user = self.create_user(data)
        self.assertNotEqual(user, None)

        redis = self.get_redis_conn()

        self.create_activate_code(redis, key, user.pk)

        data = {
            'activate_code': self.activate_code
        }

        response = self.activate_user(data, user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        activate_code = redis.get(key)

        self.assertEqual(user.is_active, True)
        self.assertEqual(activate_code, None)



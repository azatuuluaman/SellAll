from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from advertisement.utils import Redis

User = get_user_model()

API_URL = '/api/v1/'


class UserTestCase(APITestCase):
    model = User
    email = 'admin@gmail.com'
    password = 'admin12345'
    activate_code = 1234

    def test_register(self):
        data = {
            'email': self.email,
            'first_name': 'Admin',
            'last_name': 'Gmail',
            'password': self.password,
            'password_confirm': self.password
        }
        response = self.client.post(f'{API_URL}/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        key = f'activate_code_{self.activate_code}'
        user = User.objects.get(email=self.email)

        redis = Redis()
        redis.conn.set(key, user.pk)

        data = {
            'activate_code': self.activate_code
        }

        response = self.client.post(f'{API_URL}/activation/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(user.is_active, True)
        self.assertEqual(redis.conn.get(key), None)

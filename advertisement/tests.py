import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .management.commands import dump_categories
from .management.commands import parse
from .models import (
    City,
    Category,
    ChildCategory,
    Advertisement
)

User = get_user_model()

URL = 'http://localhost:8000'


def generate_url(url_name, kwargs=None):
    return f'{URL}{reverse(url_name, kwargs=kwargs)}'


class AdsTestCase(APITestCase):
    city_list = ['Bishkek', 'Osh', 'Jalal-Abad ', 'Karakol ', 'Tokmok', 'Kara-Balta']
    user_data = {
        'email': 'admin@gmail.com',
        'first_name': 'Admin',
        'last_name': 'Gmail',
        'password': 'admin',
    }

    def test_cities(self):
        url = generate_url("cities")
        self.create_cities()
        query_count = self.get_cities().count()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content).get('count'), query_count)

    def test_categories(self):
        url = generate_url("categories")
        self.create_categories_and_children()
        category_count = self.get_categories().count()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content).get('count'), category_count)

    def test_child_categories(self):
        url = generate_url("child_categories")
        self.create_categories_and_children()
        children_count = self.get_child_categories().count()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content).get('count'), children_count)

    def test_category(self):
        self.create_categories_and_children()

        for category in self.get_categories():
            url = generate_url("category", kwargs={"pk": category.pk})
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ads_complex(self):
        self.create_super_user(self.user_data)
        self.create_cities()
        self.create_categories_and_children()

        user = self.get_super_user()
        token = RefreshToken.for_user(user)

        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token.access_token}'

        cities = self.get_cities()
        categories = self.get_categories()
        child_categories = self.get_child_categories()

        ads_create_data = {
            'name': 'Ads #1',
            'price': 15000,
            'max_price': 50000,
            'description': 'Ads #1',
            'whatsapp_number': '+996505117733',
            'city': 1,
            'email': user.email,
            'type': settings.ACTIVE,
            'child_category': child_categories[0].pk,
            'owner': user.pk,
        }

        create_response = self.create_ads_endpoint(ads_create_data)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        parser = parse.Command()

        # options = {
        #     'start_page': 1,
        #     'end_page': 2
        # }
        #
        # parser.handle(**options)

        advertisement_count = self.get_ads().filter(type=settings.ACTIVE).count()
        list_response = self.ads_list_endpoint()
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(list_response.content).get('count'), advertisement_count)

        get_ads_response = self.get_ads_endpoint(pk=1)
        get_ads_data = json.loads(get_ads_response.content)
        self.assertEqual(get_ads_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_ads_data.get('name'), ads_create_data.get('name'))
        self.assertEqual(get_ads_data.get('price'), ads_create_data.get('price'))
        self.assertEqual(get_ads_data.get('max_price'), ads_create_data.get('max_price'))
        self.assertEqual(get_ads_data.get('description'), ads_create_data.get('description'))
        self.assertEqual(get_ads_data.get('whatsapp_number'), ads_create_data.get('whatsapp_number'))
        self.assertEqual(get_ads_data.get('child_category'), child_categories[0].name)
        self.assertEqual(get_ads_data.get('city'), cities[0].name)
        self.assertEqual(get_ads_data.get('type'), ads_create_data.get('type'))
        self.assertEqual(get_ads_data.get('owner').get('id'), user.pk)

        users_ads_response = self.get_users_ads()
        response_data = json.loads(get_ads_response.content)
        response_count = response_data.get('count')
        self.assertEqual(users_ads_response.status_code, status.HTTP_200_OK)
        if response_count:
            self.assertEqual(response_count, Advertisement.objects.filter(owner=user).count())

    def get_users_ads(self):
        url = generate_url('users_ads')
        response = self.client.get(url)
        return response

    def get_ads_endpoint(self, pk):
        url = generate_url("advertisement", kwargs={"pk": pk})
        response = self.client.get(url)
        return response

    def create_ads_endpoint(self, data):
        url = generate_url("ads_create")
        response = self.client.post(url, data=data)
        return response

    def ads_list_endpoint(self):
        url = generate_url("ads_list")
        response = self.client.get(url)
        return response

    def get_ads(self):
        return Advertisement.objects.all()

    def create_cities(self):
        for city in self.city_list:
            City.objects.create(name=city)

    def get_cities(self):
        return City.objects.all()

    def create_categories_and_children(self):
        command = dump_categories.Command()
        command.handle()

    def get_categories(self):
        return Category.objects.all()

    def get_child_categories(self):
        return ChildCategory.objects.all()

    def create_super_user(self, data):
        user = User.objects.create_superuser(**data)
        return user

    def get_super_user(self):
        return User.objects.get(email=self.user_data.get('email'))

import json

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .management.commands import dump_categories
from .models import (
    City,
    Category,
    ChildCategory
)

URL = 'http://localhost:8000'


class AdsTestCase(APITestCase):
    city_list = ['Bishkek', 'Osh', 'Jalal-Abad ', 'Karakol ', 'Tokmok', 'Kara-Balta']

    def create_cities(self):
        for city in self.city_list:
            City.objects.create(name=city)

        city_count = City.objects.all().count()
        return city_count

    def create_categories_and_children(self):
        command = dump_categories.Command()
        command.handle()
        category_count = Category.objects.all().count()
        children_count = ChildCategory.objects.all().count()
        return category_count, children_count

    def test_cities(self):
        url = f'{URL}{reverse("cities")}'
        query_count = self.create_cities()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content).get('count'), query_count)

    def test_categories(self):
        url = f'{URL}{reverse("categories")}'
        category_count, children_count = self.create_categories_and_children()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content).get('count'), category_count)

from rest_framework.test import APITestCase
from rest_framework import status

from .models import City


class CityTestCase(APITestCase):
    city_list = ['Bishkek', 'Osh', 'Jalal-Abad ', 'Karakol ', 'Tokmok', 'Kara-Balta']
    model = City

    def test_create_and_list(self):
        for city in self.city_list:
            data = {'name': city}
            response = self.client.post('/api/city/', data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/api/city/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.city_list), self.model.objects.count())


import json

from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework import status

from advertisement.tests import generate_url
from siteapp.models import Site, SocialMedia


class SiteAppTestCase(APITestCase):
    site_data = {
        'name': 'Zeon Bazar',
        'privacy_policy_text': 'Big text about privacy policy',
        'copyright': 'bazar'
    }

    social_media_data = {
        'name': 'telegram',
        'type': settings.SOCIAL_NETWORK,
        'link': 't.me/name',
        'site_id': None
    }

    def create_site(self):
        site = Site.objects.create(**self.site_data)
        return site

    def create_social_media(self, site):
        social_media = self.social_media_data
        social_media['site'] = site
        social_media = SocialMedia.objects.create(**social_media)
        return social_media

    def test_site(self):
        site = self.create_site()

        url = generate_url('site')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content).get('results')[0]

        self.assertEqual(data.get('name'), site.name)
        self.assertEqual(data.get('privacy_policy_text'), site.privacy_policy_text)
        self.assertEqual(data.get('copyright'), site.copyright)

    # def test_social_media(self):
    #     site = self.create_site()
    #     social_media = self.create_social_media(site)
    #
    #     url = generate_url('social_media')
    #     # print(url)
    #     response = self.client.get(url)

        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        #
        # data = json.loads(response.content).get('results')[0]
        #
        # self.assertEqual(data.get('name'), social_media.name)
        # self.assertEqual(data.get('type'), social_media.type)
        # self.assertEqual(data.get('link'), social_media.link)
        # self.assertEqual(data.get('site'), social_media.site_id)

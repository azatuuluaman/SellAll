import random

import requests
from bs4 import BeautifulSoup
from django.utils.text import slugify

from advertisement.models import Advertisement, ChildCategory
from config import settings
from user.models import User

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.143 YaBrowser/22.5.0.1878 Yowser/2.5 Safari/537.36',
}


def parse_house_kg(start, end):
    all_advertisement_list = []
    child_category = ChildCategory.objects.all()
    print('Parsing start')
    print('##############')
    for i in range(start, end + 1):
        url = f'https://www.house.kg/kupit?page={i}'
        req = requests.get(url, headers=headers)
        src = req.text

        soup = BeautifulSoup(src,
                             "lxml")
        all_advertisement_hrefs = soup.find(class_="listings-wrapper").find_all('div', class_="listing")

        for item in all_advertisement_hrefs:
            item_href = 'https://www.house.kg' + item.find('div', class_="right-info").find("div",
                                                                                            class_="top-info").find(
                "div", class_="left-side").find(
                "p", class_="title").find('a').get("href")

            all_advertisement_list.append(item_href)

    print('Add data to database')
    print('##############')
    for url in all_advertisement_list:
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")

        try:
            advertisement_name = soup.find(class_="details-main").find("div", class_="details-stat-block") \
                .find('p', class_="title").get_text(strip=True)
            advertisement_price = int(''.join(soup.find(class_="details-main").find("div", class_="details-stat-block") \
                                              .find("p", class_="price").find('span', class_="dollars").find(
                "span").get_text(strip=True).strip('$').split()))
            advertisement_number = soup.find(class_="phone-fixable-block").find("div", class_="right") \
                .find("div", class_="number").get_text(strip=True)
            ads_owner = User.objects.first()
            advertisement_description = soup.find(class_="details-main").find('div', class_="right").find \
                ("div", class_="description").find("p").get_text(strip=True)

            slug = slugify(f'{advertisement_name}-{ads_owner.pk}', allow_unicode=True)

            if Advertisement.objects.filter(slug=slug).exists():
                continue

            random_num = random.randint(1, child_category.count())
            Advertisement.objects.create(name=advertisement_name, price=advertisement_price,
                                         whatsapp_number=advertisement_number, owner=ads_owner,
                                         description=advertisement_description, type=settings.ACTIVE,
                                         child_category=child_category[random_num])
        except Exception:
            continue

    print('End!')

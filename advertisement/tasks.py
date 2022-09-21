import random
import requests

from bs4 import BeautifulSoup
from django.utils.text import slugify

from advertisement.models import Advertisement, ChildCategory
from config import settings
from config.celery import app
from user.models import User

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.143 YaBrowser/22.5.0.1878 Yowser/2.5 Safari/537.36',
}


@app.task
def parse_house_kg(start, end):
    count = 0
    all_advertisement_list = []
    child_category = ChildCategory.objects.all()
    for i in range(start, end + 1):
        print(count)
        count += 1
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


headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.143 YaBrowser/22.5.0.1878 Yowser/2.5 Safari/537.36',
}


def get_descrition(POSTSOUD):
    desc = POSTSOUD.find_all(class_='desc')
    if desc:
        return desc[1].text


@app.task
def parse_doska():
    all_advertisement_list = []
    print("Start Parsing")
    for i in range(1, 2):
        url = f'https://resume.doska.kg/vacancy/&page={i}&sortby=new'
        req = requests.get(url, headers=headers)
        src = req.text

        soup = BeautifulSoup(src, "lxml")

        all_advertisement_hrefs = soup.find('div', class_='main').find('div', id='wrapper-doska') \
            .find_all('div', class_='list_full_title')

        for item in all_advertisement_hrefs:
            item_href = 'https://resume.doska.kg' + item.find('a', class_='title_url').get('href')

            all_advertisement_list.append(item_href)

    for url in all_advertisement_list:
        # print('Data adding...')
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")

        # try:
        advertisement_name = soup.find('div', class_='main').find('div', id='wrapper-doska'). \
            find('div', class_='left-col-block').find('div', class_='title').get_text(strip=True)

        advertisement_number = soup.find('div', class_='main').find('div', id='wrapper-doska'). \
            find('div', class_='left-col-block').find('div', class_='desc').get_text(strip=True)

        clean_number = "".join(c for c in advertisement_number if c.isdecimal())

        ads_owner = User.objects.first()

        desc = get_descrition(soup)

        Advertisement.objects.create(name=advertisement_name, whatsapp_number=clean_number,
                                     type=settings.ACTIVE, description=desc, owner=ads_owner)


@app.task
def parse_salexy():
    all_advertisement_list = []
    print("Start Parsing")
    for i in range(1, 2):
        url = f'https://salexy.kg/bishkek/rabota/ishu_rabotu?page={i}'
        req = requests.get(url, headers=headers)
        src = req.text

        soup = BeautifulSoup(src,
                             "lxml")
        all_advertisement_hrefs = soup.find('ul', class_='product-list').find_all('div', class_='content')

        for item in all_advertisement_hrefs:
            item_href = item.find('div', class_='top-info').find('div', class_='info-content').find('div',
                                                                                                    class_='title') \
                .find('a').get('href')

            all_advertisement_list.append(item_href)

    for url in all_advertisement_list:
        print("Data adding...")
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")

        try:
            advertisement_name = soup.find('div', id='main').find('div', class_='product-title-holder') \
                .find('div', class_='content').find('h1', class_='product-name').get_text(strip=True)

            advertisement_price = int(''.join(soup.find('div', id='main').find('div', class_='product-title-holder') \
                                              .find('div', class_='control-holder').find('span',
                                                                                         class_='price').get_text(
                strip=True).strip('KGS').split()))

            ads_owner = User.objects.first()

            advertisement_description = str(soup.find('div', id='main').find('div', class_="two-columns-holder") \
                                            .find('div', class_='product').find('div', class_='info').find('div',
                                                                                                           class_='description').get_text(
                strip=True)).strip(' ')

            Advertisement.objects.create(name=advertisement_name, price=advertisement_price,
                                         owner=ads_owner,
                                         description=advertisement_description, type=settings.ACTIVE,
                                         )
            print("Success added!")

        except Exception:
            advertisement_price = 0
            print(advertisement_price)

            continue
        print(advertisement_price)

    print('Parsing finished!')

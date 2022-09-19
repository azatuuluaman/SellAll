# Generated by Django 4.1 on 2022-09-19 06:15

import cloudinary.models
import django.contrib.postgres.fields
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdsComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Комментарий')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Последняя дата изменения')),
            ],
            options={
                'verbose_name': 'Коментарий',
                'verbose_name_plural': 'Коментарии',
                'ordering': ['created_on'],
            },
        ),
        migrations.CreateModel(
            name='AdsImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Фотография')),
            ],
            options={
                'verbose_name': 'Изображение объявления',
                'verbose_name_plural': 'Изображения объявлений',
            },
        ),
        migrations.CreateModel(
            name='AdsSubscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='Дата начала')),
                ('end_date', models.DateTimeField(verbose_name='Дата окончания')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Подписка объявления',
                'verbose_name_plural': 'Подписки объявлений',
            },
        ),
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название товара')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('max_price', models.PositiveIntegerField(blank=True, null=True, verbose_name='Цена до')),
                ('description', models.TextField(max_length=4000, verbose_name='Ваше сообщение')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='E-mail')),
                ('phone_numbers', django.contrib.postgres.fields.ArrayField(base_field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона'), blank=True, null=True, size=8)),
                ('whatsapp_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='W/A номер')),
                ('type', models.CharField(choices=[('Активный', 'Активный'), ('На проверке', 'На проверке'), ('Неактивный', 'Неактивный')], default='На проверке', max_length=20, verbose_name='Статус объявления')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Последняя дата изменения')),
                ('disable_date', models.DateTimeField(blank=True, null=True, verbose_name='Неактивен с')),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Категория')),
                ('icon', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Иконка')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='ChildCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Под-категория')),
            ],
            options={
                'verbose_name': 'Под-категория',
                'verbose_name_plural': 'Под-категории',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='ComplainingForAds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Неверная рубрика', 'Неверная рубрика'), ('Запрещенный товар/услуга', 'Запрещенный товар/услуга'), ('Объявление не актуально', 'Объявление не актуально'), ('Неверный адрес', 'Неверный адрес'), ('Другое', 'Другое')], default='Неверная рубрика', max_length=100, verbose_name='Тип жалобы')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст')),
                ('send_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
                ('checked_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата проверки')),
                ('is_checked', models.BooleanField(default=False, verbose_name='Проверен')),
            ],
            options={
                'verbose_name': 'Жалоба',
                'verbose_name_plural': 'Жалобы',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('icon', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Иконка')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advertisements', models.ManyToManyField(related_name='favorites', to='advertisement.advertisement', verbose_name='Объявление')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранные',
            },
        ),
    ]

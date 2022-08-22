from django.conf import settings
from django.db import models
from datetime import date


def get_upload_path_ad_image(instance, filename):
    today = date.today()
    return f"ad_images/{today.year}/{today.month}/{today.day}/{instance.advertisement.username()}/{filename}"


class Category(models.Model):
    name = models.CharField('Категория', max_length=100)
    icon = models.ImageField('Иконка')


class ChildCategory(models.Model):
    name = models.CharField('Под-категория', max_length=100)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='Категория')


class Advertisement(models.Model):
    name = models.CharField('Название товара', max_length=100)
    price = models.PositiveIntegerField('Цена')
    max_price = models.PositiveIntegerField('Цена до')
    description = models.TextField('Ваше сообщение', max_length=4000)
    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True)
    email = models.EmailField('E-mail')
    whatsapp_number = models.CharField('W/A номер', max_length=20)

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    modified_at = models.DateTimeField('Дата изменения', auto_now=True)
    deleted_at = models.DateTimeField('Дата удаления', null=True, blank=True)

    child_category = models.ForeignKey(ChildCategory, on_delete=models.DO_NOTHING, verbose_name='Подкатегория')
    favourites = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        verbose_name='Избранные',
                                        related_name='favourites',
                                        blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name='Автор')


class AdsSubscribers(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.DO_NOTHING, verbose_name='Объявление')
    type = models.CharField('Тип', max_length=10)
    start_date = models.DateTimeField('Дата начала')
    end_date = models.DateTimeField('Дата окончания')
    created_at = models.DateTimeField('Дата создания', auto_now=True)


class AdsImage(models.Model):
    image = models.ImageField('Фотография', upload_to=get_upload_path_ad_image)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name='Фотографии',
                                      help_text='Объявления с фото получают в среднем в 3-5 раз больше '
                                                'откликов. Вы можете загрузить до 8 фотографий')


class Cities(models.Model):
    name = models.CharField(max_length=100)


class Number(models.Model):
    number = models.CharField('Номер', max_length=20)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name='Объявление')


class ViewStatistics(models.Model):
    views_count = models.PositiveIntegerField('Число просмотров')
    contact_view_count = models.PositiveIntegerField('Статистика просмотров контактов')
    date = models.DateField('Дата', auto_now=True)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.DO_NOTHING, verbose_name='Объявление')

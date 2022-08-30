from django.conf import settings
from django.db import models
from django.utils import timezone

from datetime import date


def get_upload_path_ad_image(instance, filename):
    today = date.today()
    return f"ad_images/{today.year}/{today.month}/{today.day}/{instance.advertisement.name}/{filename}"


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Category(models.Model):
    name = models.CharField('Категория', max_length=100)
    icon = models.ImageField('Иконка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class ChildCategory(models.Model):
    name = models.CharField('Под-категория', max_length=100)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='Категория',
                                 related_name='child_category')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Под-категория'
        verbose_name_plural = 'Под-категории'


class Advertisement(models.Model):
    name = models.CharField('Название товара', max_length=100)
    price = models.PositiveIntegerField('Цена')
    max_price = models.PositiveIntegerField('Цена до', null=True, blank=True)
    description = models.TextField('Ваше сообщение', max_length=4000)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    email = models.EmailField('E-mail')
    whatsapp_number = models.CharField('W/A номер', max_length=20)

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    modified_at = models.DateTimeField('Дата изменения', auto_now=True)
    deleted_at = models.DateTimeField('Дата удаления', null=True, blank=True)

    is_delete = models.BooleanField('Удален', default=False)

    child_category = models.ForeignKey(ChildCategory, on_delete=models.DO_NOTHING, verbose_name='Подкатегория')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name='Автор')

    def save(self, *args, **kwargs):
        # Проверка на удаление
        if self.is_delete:
            self.deleted_at = timezone.now()
        else:
            self.deleted_at = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Subscription(models.Model):
    name = models.CharField('Название', max_length=100)
    icon = models.ImageField('Иконка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class AdsSubscriber(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.DO_NOTHING, verbose_name='Объявление')
    subscription = models.ForeignKey(Subscription, on_delete=models.DO_NOTHING, verbose_name='Подписка')
    start_date = models.DateTimeField('Дата начала')
    end_date = models.DateTimeField('Дата окончания')
    created_at = models.DateTimeField('Дата создания', auto_now=True)

    def __str__(self):
        return self.advertisement.name

    class Meta:
        verbose_name = 'Подписка объявления'
        verbose_name_plural = 'Подписки объявлений'


class AdsImage(models.Model):
    image = models.ImageField('Фотография', upload_to=get_upload_path_ad_image)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name='Фотографии',
                                      help_text='Объявления с фото получают в среднем в 3-5 раз больше '
                                                'откликов. Вы можете загрузить до 8 фотографий',
                                      related_name='images')

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name = 'Изображение объявления'
        verbose_name_plural = 'Изображения объявлений'


class Number(models.Model):
    number = models.CharField('Номер', max_length=20)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name='Объявление')

    def __str__(self):
        return self.advertisement.name

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'


class ViewStatistic(models.Model):
    views_count = models.PositiveIntegerField('Число просмотров')
    contact_view_count = models.PositiveIntegerField('Статистика просмотров контактов')
    date = models.DateField('Дата', auto_now=True)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.DO_NOTHING, verbose_name='Объявление')

    def __str__(self):
        return self.advertisement.name

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'

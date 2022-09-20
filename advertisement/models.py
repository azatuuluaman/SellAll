import random

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

from phonenumber_field.modelfields import PhoneNumberField
from cloudinary.models import CloudinaryField


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Category(models.Model):
    name = models.CharField('Категория', max_length=100)
    icon = CloudinaryField('Иконка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class ChildCategory(models.Model):
    name = models.CharField('Под-категория', max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Категория',
                                 related_name='child_categories', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Под-категория'
        verbose_name_plural = 'Под-категории'


class Advertisement(models.Model):
    name = models.CharField('Название товара', max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    price = models.PositiveIntegerField('Цена')
    max_price = models.PositiveIntegerField('Цена до', null=True, blank=True)
    description = models.TextField('Ваше сообщение', max_length=4000)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField('E-mail', null=True)
    phone_numbers = ArrayField(PhoneNumberField('Номер телефона'), size=8, null=True, blank=True)
    whatsapp_number = PhoneNumberField('W/A номер')

    type = models.CharField('Статус объявления', max_length=20,
                            choices=settings.ADS_CHOICES, default=settings.CHECKING)

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    modified_at = models.DateTimeField('Последняя дата изменения', auto_now=True)
    disable_date = models.DateTimeField('Неактивен с', null=True, blank=True)

    child_category = models.ForeignKey(ChildCategory, on_delete=models.SET_NULL, verbose_name='Подкатегория',
                                       blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Автор', blank=True,
                              null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Проверка на удаление
        if self.type == settings.DISABLE:
            self.disable_date = timezone.now()
        else:
            self.disable_date = None

        if self._state.adding:
            self.slug = slugify(f'{self.name}-{random.randint(1000, 9999)}', allow_unicode=True)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['id']


class Subscription(models.Model):
    name = models.CharField('Название', max_length=100)
    icon = CloudinaryField('Иконка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['id']


class AdsSubscriber(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.SET_NULL, verbose_name='Объявление', blank=True,
                                      null=True, related_name='subscriber')
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, verbose_name='Подписка', blank=True,
                                     null=True)
    start_date = models.DateTimeField('Дата начала')
    end_date = models.DateTimeField('Дата окончания')
    created_at = models.DateTimeField('Дата создания', auto_now=True)

    def __str__(self):
        return self.advertisement.name

    class Meta:
        verbose_name = 'Подписка объявления'
        verbose_name_plural = 'Подписки объявлений'
        ordering = ['id']


class AdsImage(models.Model):
    image = CloudinaryField('Фотография')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name='Объявление',
                                      help_text='Объявления с фото получают в среднем в 3-5 раз больше '
                                                'откликов. Вы можете загрузить до 8 фотографий',
                                      related_name='images')

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name = 'Изображение объявления'
        verbose_name_plural = 'Изображения объявлений'
        ordering = ['id']


class Favorite(models.Model):
    advertisements = models.ForeignKey(Advertisement, verbose_name='Объявление', on_delete=models.CASCADE,
                                       related_name='favorites')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                verbose_name='Пользователь', related_name='favorites')

    def __str__(self):
        return f'{self.user.email}-{self.advertisements}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        ordering = ['id']


class AdsComment(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='comments',
                                      verbose_name='Объявление')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField('Комментарий')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children',
                               verbose_name='Родительский комментарий', null=True, blank=True)
    created_on = models.DateTimeField('Дата создания', auto_now_add=True)
    modified_at = models.DateTimeField('Последняя дата изменения', auto_now=True)

    def __str__(self):
        return f'Comment {self.advertisement} by {self.user}'

    def children(self):
        return AdsComment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ['created_on']


class ComplainingForAds(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField("Тип жалобы", max_length=100, choices=settings.COMPLAINING_TYPE,
                            default=settings.WRONG_RUBRIC)
    text = models.TextField('Текст', null=True, blank=True)
    send_date = models.DateTimeField('Дата отправки', auto_now_add=True)
    checked_at = models.DateTimeField('Дата проверки', null=True, blank=True)

    is_checked = models.BooleanField('Проверен', default=False)

    def save(self, *args, **kwargs):
        if self.is_checked:
            self.checked_at = timezone.now()
        else:
            self.checked_at = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.advertisement.pk} - {self.type}'

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'
        ordering = ['id']

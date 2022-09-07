from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

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
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='Категория',
                                 related_name='child_categories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Под-категория'
        verbose_name_plural = 'Под-категории'


class Advertisement(models.Model):
    class Type(models.TextChoices):
        ACTIVE = 'Активный', 'Активный'
        CHECKING = 'На проверке', 'На проверке'
        DISABLE = 'Неактивен', 'Неактивен'

    name = models.CharField('Название товара', max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    price = models.PositiveIntegerField('Цена')
    max_price = models.PositiveIntegerField('Цена до', null=True, blank=True)
    description = models.TextField('Ваше сообщение', max_length=4000)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    email = models.EmailField('E-mail')
    whatsapp_number = models.CharField('W/A номер', max_length=20)
    type = models.CharField('Статус объявления', max_length=20, choices=Type.choices, default=Type.CHECKING)

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    modified_at = models.DateTimeField('Последняя дата изменения', auto_now=True)
    deleted_at = models.DateTimeField('Дата удаления', null=True, blank=True)

    is_delete = models.BooleanField('Удален', default=False)

    child_category = models.ForeignKey(ChildCategory, on_delete=models.DO_NOTHING, verbose_name='Подкатегория')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name='Автор')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Проверка на удаление
        if self.is_delete:
            self.deleted_at = timezone.now()
        else:
            self.deleted_at = None

        self.slug = slugify(f'{self.name}-{self.id}')

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Subscription(models.Model):
    name = models.CharField('Название', max_length=100)
    icon = CloudinaryField('Иконка')

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


class PhoneNumber(models.Model):
    phone_number = models.CharField('Номер', max_length=20)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE,
                                      verbose_name='Объявление', related_name='phone_numbers')

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


class Favorites(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE,
                                      verbose_name='Объявление', related_name='favorites')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='Пользователь', related_name='favorites')

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


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
        return f'Comment {self.text} by {self.user}'

    def children(self):
        return AdsComment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Кометарии'
        ordering = ['created_on']

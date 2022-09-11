from django.db import models

from cloudinary.models import CloudinaryField


class Site(models.Model):
    name = models.CharField('Название сайта', max_length=100)
    logo = CloudinaryField('Логотип')
    privacy_policy_text = models.TextField('Политика конфиденциальности текст', max_length=5000)
    copyright = models.CharField('Авторские права', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Информация о сайте'
        verbose_name_plural = 'Информация о сайтах'


class SocialMedia(models.Model):
    class Type(models.TextChoices):
        SOCIAL_NETWORK = 'Social Networks', 'Social Networks'
        APP = 'App', 'App'

    name = models.CharField('Название', max_length=100)
    image = CloudinaryField('Изображение')
    type = models.CharField('Тип', max_length=20, choices=Type.choices, default=Type.SOCIAL_NETWORK)
    link = models.CharField('Ссылка', max_length=100)
    site = models.ForeignKey(Site, verbose_name='Сайт', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Cоц-медия'
        verbose_name_plural = 'Соц-медии'


class FeedBack(models.Model):
    class Subject(models.TextChoices):
        CLAIM = 'Жалоба', 'Жалоба'
        OFFER = 'Предложение', 'Предложение'

    name = models.CharField('Имя', max_length=100)
    email = models.EmailField()
    subject = models.CharField('Тема сообщения', max_length=20, choices=Subject.choices, default=Subject.CLAIM)
    text = models.TextField('Сообщение', max_length=5000)
    send_date = models.DateTimeField('Дата отправки', auto_now_add=True)
    check_date = models.DateTimeField('Дата проверки', null=True, blank=True)
    checked = models.BooleanField('Проверена', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'


class HelpCategory(models.Model):
    name = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория помощи'
        verbose_name_plural = 'Категории помощи'


class Help(models.Model):
    title = models.CharField('Загаловок', max_length=100)
    text = models.TextField('Текст', max_length=5000)
    category = models.ForeignKey(HelpCategory, on_delete=models.DO_NOTHING, related_name='help',
                                 verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Помощь'
        verbose_name_plural = 'Помощь'


from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.crypto import get_random_string

from advertisement.models import Advertisement


class UserManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name, phone_number, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        if not first_name:
            raise ValueError('User must have an name')

        if not last_name:
            raise ValueError('User must have an surname')

        if not phone_number:
            raise ValueError('User must have an phone number')

        email = self.normalize_email(email)

        user = self.model(email=email,
                          first_name=first_name,
                          last_name=last_name,
                          phone_number=phone_number,
                          **extra_fields)

        user.set_password(password)

        user.save(using=self._db)
        return user

    def create(self, email, first_name, last_name, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, first_name, last_name, phone_number, password, **extra_fields)

    def create_superuser(self, email, first_name, last_name, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(email, first_name, last_name, phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField('Name', max_length=100)
    last_name = models.CharField('Surname', max_length=100)
    phone_number = models.CharField('Phone number', max_length=20)

    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    favourites = models.ManyToManyField(Advertisement, verbose_name='Избранные', related_name='favourites', blank=True)

    activation_code = models.CharField(max_length=8, blank=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = (
        'first_name',
        'last_name',
        'phone_number'
    )

    ordering = ('created',)

    def has_module_perms(self, app_label):
        return self.is_staff or self.is_superuser

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def create_activation_code(self):
        code = get_random_string(8)
        if User.objects.filter(activation_code=code).exists():
            self.create_activation_code()
        self.activation_code = code
        self.save(update_fields=['activation_code'])

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

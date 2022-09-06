from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.crypto import get_random_string
from django.db import models

from advertisement.models import Advertisement

from .manager import UserManager


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

    activation_code = models.CharField(max_length=8, blank=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = (
        'first_name',
        'last_name',
        'phone_number'
    )

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

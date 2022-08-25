from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import Permission
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not first_name:
            raise ValueError('User must have an name')

        if not last_name:
            raise ValueError('User must have an surname')

        if not phone_number:
            raise ValueError('User must have an phone number')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )

        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, password):
        user = self.create_user(email, first_name, last_name, phone_number, password=password)

        user.is_active = True
        user.is_admin = True
        user.is_superuser = True

        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField('Name', max_length=100)
    last_name = models.CharField('Surname', max_length=100)
    phone_number = models.CharField('Phone number', max_length=20)

    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField('active', default=False)
    is_admin = models.BooleanField('admin', default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = (
        'first_name',
        'last_name',
        'phone_number'
    )

    ordering = ('created',)

    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    def __unicode__(self):
        return self.email

# class Profile(models.Model):
#     GENDER = (
#         ('M', 'Homme'),
#         ('F', 'Femme'),
#     )
#
#     user = models.OneToOneField(settings.AUTH_USER_MODEL)
#     first_name = models.CharField(max_length=120, blank=False)
#     last_name = models.CharField(max_length=120, blank=False)
#     gender = models.CharField(max_length=1, choices=GENDER)
#     zip_code = models.CharField(max_length=5, validators=[MinLengthValidator(5)], blank=False)
#
#     def __unicode__(self):
#         return u'Profile of user: {0}'.format(self.user.email)


# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
# post_save.connect(create_profile, sender=User)
#
#
# def delete_user(sender, instance=None, **kwargs):
#     try:
#         instance.user
#     except User.DoesNotExist:
#         pass
#     else:
#         instance.user.delete()
# post_delete.connect(delete_user, sender=Profile)

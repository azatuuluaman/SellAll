# Generated by Django 4.1 on 2022-08-24 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('user', '0004_remove_user_verified_alter_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='permission',
            field=models.ManyToManyField(related_name='users', to='auth.permission'),
        ),
    ]
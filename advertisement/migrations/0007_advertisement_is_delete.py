# Generated by Django 4.1 on 2022-08-26 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0006_alter_advertisement_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Удален'),
        ),
    ]
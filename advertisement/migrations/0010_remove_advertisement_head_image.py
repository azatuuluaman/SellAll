# Generated by Django 4.1 on 2022-08-29 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0009_alter_childcategory_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisement',
            name='head_image',
        ),
    ]

# Generated by Django 4.1 on 2022-08-24 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siteapp', '0002_alter_feedback_subject'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'verbose_name': 'Обратная связь', 'verbose_name_plural': 'Обратная связь'},
        ),
        migrations.AlterModelOptions(
            name='help',
            options={'verbose_name': 'Помощь', 'verbose_name_plural': 'Помощь'},
        ),
        migrations.AlterModelOptions(
            name='site',
            options={'verbose_name': 'Информация о сайте', 'verbose_name_plural': 'Информация о сайтах'},
        ),
        migrations.AlterModelOptions(
            name='socialmedia',
            options={'verbose_name': 'Cоц-медия', 'verbose_name_plural': 'Соц-медии'},
        ),
        migrations.RemoveField(
            model_name='site',
            name='privacy_policy_title',
        ),
    ]
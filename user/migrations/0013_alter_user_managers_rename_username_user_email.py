# Generated by Django 4.1 on 2022-08-30 01:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_rename_email_user_username'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='email',
        ),
    ]

from django.conf import settings
from django.core.management import BaseCommand

from siteapp.models import HelpCategory, Help


class Command(BaseCommand):
    def handle(self, *args, **options):
        text_path = settings.BASE_DIR / 'siteapp/management/static/files'

        if not text_path.is_dir():
            print('Text for help not found!')
            return

        category_name = {
            'Объявления': [
                (1, 'Редактировать объявление'),
                (2, 'Размещение объявлений')
            ],
            'Магазины': [
                (1, 'Редактировать объявление'),
                (2, 'Импорт объявлений'),
                (2, 'Импорт объявлений 3456'),
                (2, 'Импорт объявлений 564'),
                (2, 'Импорт объявлений 321'),
                (2, 'Импорт объявлений 123'),
            ],
            'Аккаунт': [
                (1, 'Восстановить пароль'),
                (2, 'Изменить электронную почту'),
                (2, 'Удалить учетную запись'),
            ],
            'Платные услуги': [
                (1, 'Платные услуги'),
                (1, 'Восстановить пароль'),
                (1, 'Платные услуги'),
                (1, 'Платные услуги'),
            ]
        }
        for i, name in enumerate(category_name.keys()):
            category = HelpCategory.objects.create(name=name)
            for j, title in category_name[name]:
                with open(f'{text_path}/{i+1}.{j}.txt', 'r') as text:
                    Help.objects.create(title=title, text=text.read(), category=category)

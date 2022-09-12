from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings

from advertisement.models import Category, ChildCategory


class Command(BaseCommand):
    def handle(self, *args, **options):
        # with open(f'{settings.BASE_DIR}/advertisement/management/commands/static/icon/electronics.svg', mode='rb') as f:
        #     category = Category.objects.create(name='Электроника', icon=File(f))
        category = Category.objects.create(name='Электроника')
        ChildCategory.objects.create(category=category, name='Телефоны и аксессуары')
        ChildCategory.objects.create(category=category, name='Фото / видео')
        ChildCategory.objects.create(category=category, name='Аудиотехника')
        ChildCategory.objects.create(category=category, name='Техника для дома')
        ChildCategory.objects.create(category=category, name='Аудиотехника')
        ChildCategory.objects.create(category=category, name='Индивидуальный уход')
        ChildCategory.objects.create(category=category, name='Компьютеры')
        ChildCategory.objects.create(category=category, name='Техника для кухни')
        ChildCategory.objects.create(category=category, name='Прочая электроника')
        ChildCategory.objects.create(category=category, name='Игры и игровые приставки')
        ChildCategory.objects.create(category=category, name='Климатическое оборудование')
        ChildCategory.objects.create(category=category, name='Ремонт и обслуживание техники')
        ChildCategory.objects.create(category=category, name='Ноутбуки и аксессуары')

        # with open(f'{settings.BASE_DIR}/advertisement/management/commands/static/icon/estate.svg.svg', mode='rb') as f:
        #     category = Category.objects.create(name='Недвижимость', icon=File(f))
        category = Category.objects.create(name='Недвижимость')
        ChildCategory.objects.create(category=category, name='Продажа недвижимости')
        ChildCategory.objects.create(category=category, name='Аренда недвижимости')
        ChildCategory.objects.create(category=category, name='Коммерческая недвижимость')
        ChildCategory.objects.create(category=category, name='Недвижимость за рубежом')

        # with open(f'{settings.BASE_DIR}/advertisement/management/commands/static/icon/transport.svg', mode='rb') as f:
        #     category = Category.objects.create(name='Транспорт', icon=File(f))
        category = Category.objects.create(name='Транспорт')
        ChildCategory.objects.create(category=category, name='Легковые автомобили')
        ChildCategory.objects.create(category=category, name='Запчасти')
        ChildCategory.objects.create(category=category, name='Прочее')
        ChildCategory.objects.create(category=category, name='Мото')
        ChildCategory.objects.create(category=category, name='Аксессуары')
        ChildCategory.objects.create(category=category, name='Грузовики и спецтехника')
        ChildCategory.objects.create(category=category, name='Автоуслуги')

        # with open(f'{settings.BASE_DIR}/advertisement/management/commands/static/icon/busines.svg', mode='rb') as f:
        #     category = Category.objects.create(name='Бизнес и работа', icon=File(f))
        category = Category.objects.create(name='Бизнес и работа')
        ChildCategory.objects.create(category=category, name='Все для офиса')
        ChildCategory.objects.create(category=category, name='Оборудование')
        ChildCategory.objects.create(category=category, name='Бизнес образование')
        ChildCategory.objects.create(category=category, name='Товары')
        ChildCategory.objects.create(category=category, name='Продажа бизнеса')
        ChildCategory.objects.create(category=category, name='Партнерство, инвестиции')
        ChildCategory.objects.create(category=category, name='Сырье / материалы')
        ChildCategory.objects.create(category=category, name='Услуги для бизнесы')
        ChildCategory.objects.create(category=category, name='Прочее')

        # with open(f'{settings.BASE_DIR}/advertisement/management/commands/static/icon/dress.svg', mode='rb') as f:
        #     category = Category.objects.create(name='Личные вещи', icon=File(f))
        category = Category.objects.create(name='Личные вещи')
        ChildCategory.objects.create(category=category, name='Одежда, обувь')
        ChildCategory.objects.create(category=category, name='Аксессуары')
        ChildCategory.objects.create(category=category, name='Для свадьбы')
        ChildCategory.objects.create(category=category, name='Подарки')
        ChildCategory.objects.create(category=category, name='Наручные часы')
        ChildCategory.objects.create(category=category, name='Красота / здоровье')

        # with open(f'{settings.BASE_DIR}/advertisement/management/commands/static/icon/animals.svg', mode='rb') as f:
        category = Category.objects.create(name='Зверюшки')
        ChildCategory.objects.create(category=category, name='Собаки')
        ChildCategory.objects.create(category=category, name='Кошки')
        ChildCategory.objects.create(category=category, name='Грызуны')
        ChildCategory.objects.create(category=category, name='Аквариумные рыбки')
        ChildCategory.objects.create(category=category, name='Птицы')
        ChildCategory.objects.create(category=category, name='Сельхоз животные')
        ChildCategory.objects.create(category=category, name='Товары для животных')
        ChildCategory.objects.create(category=category, name='Другие животные')

        # with open(f'{settings.BASE_DIR}/advertisement/management/commands/static/icon/house.svg', mode='rb') as f:
        category = Category.objects.create(name='Дом и дача')
        ChildCategory.objects.create(category=category, name='Строительство / ремонт')
        ChildCategory.objects.create(category=category, name='Садовые растение')
        ChildCategory.objects.create(category=category, name='Хозяйственные инвентарь')
        ChildCategory.objects.create(category=category, name='Текстиль и ковры')
        ChildCategory.objects.create(category=category, name='Инструменты')
        ChildCategory.objects.create(category=category, name='Садовые инвентарь')
        ChildCategory.objects.create(category=category, name='Прочие товары')
        ChildCategory.objects.create(category=category, name='Продукты питания, напитки')
        ChildCategory.objects.create(category=category, name='Комнатные растения')
        ChildCategory.objects.create(category=category, name='Садоводство - прочее')
        ChildCategory.objects.create(category=category, name='Товары дома и отдыха')

        # with open(f'{settings.BASE_DIR}/advertisement/management/commands/static/icon/services.svg', mode='rb') as f:
        #     category = Category.objects.create(name='Услуги', icon=File(f))
        category = Category.objects.create(name='Услуги')
        ChildCategory.objects.create(category=category, name='IT, интернет, телеком')
        ChildCategory.objects.create(category=category, name='Обучение, курсы')
        ChildCategory.objects.create(category=category, name='Ремонт и обслуживание техники')
        ChildCategory.objects.create(category=category, name='Прокат товаров')
        ChildCategory.objects.create(category=category, name='Строительство, ремонт')
        ChildCategory.objects.create(category=category, name='Развлечение, фото, видео')
        ChildCategory.objects.create(category=category, name='Деловые, услуги')
        ChildCategory.objects.create(category=category, name='Прочие услуги')
        ChildCategory.objects.create(category=category, name='Красота, здоровье')
        ChildCategory.objects.create(category=category, name='Туризм, иммиграция')
        ChildCategory.objects.create(category=category, name='Безопасность, детективы')

        # with open(f'{settings.BASE_DIR}/advertisement/management/commands/static/icon/beach.svg', mode='rb') as f:
        #     category = Category.objects.create(name='Отдых и спорт', icon=File(f))
        category = Category.objects.create(name='Отдых и спорт')
        ChildCategory.objects.create(category=category, name='Антиквариат, коллекции')
        ChildCategory.objects.create(category=category, name='Книги и журнали')
        ChildCategory.objects.create(category=category, name='Музыкальные инструменты')
        ChildCategory.objects.create(category=category, name='Билеты и путешествия')
        ChildCategory.objects.create(category=category, name='Спорт, отдых')
        ChildCategory.objects.create(category=category, name='Поиск групп, музыкантов')

        # with open(f'{settings.BASE_DIR}/advertisement/management/commands/static/icon/children.svg', mode='rb') as f:
        #     category = Category.objects.create(name='Детский мир', icon=File(f))
        category = Category.objects.create(name='Детский мир')
        ChildCategory.objects.create(category=category, name='Детская одежда')
        ChildCategory.objects.create(category=category, name='Детские автокресла')
        ChildCategory.objects.create(category=category, name='Детский транспорт')
        ChildCategory.objects.create(category=category, name='Прочие детские товары')
        ChildCategory.objects.create(category=category, name='Детская обувь')
        ChildCategory.objects.create(category=category, name='Детские мебель')
        ChildCategory.objects.create(category=category, name='Кормление')
        ChildCategory.objects.create(category=category, name='Детские коляски')
        ChildCategory.objects.create(category=category, name='Игрушки')
        ChildCategory.objects.create(category=category, name='Товары для школьников')

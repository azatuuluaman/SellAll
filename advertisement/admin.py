from django.contrib import admin
from .models import Category, ChildCategory, Advertisement, AdsSubscriber, AdsImage,\
    City, Number, ViewStatistic

admin.site.register(Category)
admin.site.register(ChildCategory)
admin.site.register(Advertisement)
admin.site.register(AdsSubscriber)
admin.site.register(AdsImage)
admin.site.register(City)
admin.site.register(Number)
admin.site.register(ViewStatistic)
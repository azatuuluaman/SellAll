from django.contrib import admin
from .models import Category, ChildCategory, Advertisement, AdsSubscribers, AdsImage,\
    Cities, Number, ViewStatistics

admin.site.register(Category)
admin.site.register(ChildCategory)
admin.site.register(Advertisement)
admin.site.register(AdsSubscribers)
admin.site.register(AdsImage)
admin.site.register(Cities)
admin.site.register(Number)
admin.site.register(ViewStatistics)
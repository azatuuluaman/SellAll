from django.contrib import admin

from .models import (
    Category,
    ChildCategory,
    Advertisement,
    AdsSubscriber,
    AdsImage,
    City,
    Number,
    ViewStatistic,
    Subscription
)


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_prices', 'created_at', 'modified_at', 'deleted_at', 'is_delete')
    list_display_links = ('id', 'name')
    list_editable = ('is_delete',)
    list_filter = ('city', 'child_category', 'owner', 'created_at', 'modified_at', 'deleted_at', 'is_delete')
    search_fields = ('name', 'description', 'email')
    readonly_fields = ('deleted_at',)

    def get_prices(self, obj):
        return f'{obj.price}-{obj.max_price}' if obj.max_price else obj.price

    get_prices.short_description = 'Цена'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon')
    list_display_links = ('id', 'name')


@admin.register(ChildCategory)
class ChildCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('category',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(AdsSubscriber)
class AdsSubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'advertisement', 'subscription', 'start_date', 'end_date', 'created_at')
    list_display_links = ('id', 'advertisement', 'subscription')
    search_fields = ('advertisement', 'subscription')
    list_filter = ('advertisement', 'subscription', 'start_date', 'end_date', 'created_at')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Number)
class NumberAdmin(admin.ModelAdmin):
    list_display = ('id', 'advertisement', 'number')
    list_display_links = ('id', 'advertisement', 'number')
    list_filter = ('advertisement',)
    search_fields = ('advertisement', 'number')


@admin.register(ViewStatistic)
class ViewStatisticAdmin(admin.ModelAdmin):
    list_display = ('advertisement', 'views_count', 'contact_view_count', 'date')
    list_display_links = ('advertisement',)
    list_filter = ('advertisement', 'date')
    search_fields = ('advertisement', 'date')


@admin.register(AdsImage)
class AdsImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'advertisement', 'image')
    list_display_links = ('id', 'advertisement')
    list_filter = ('advertisement',)
    search_fields = ('advertisement',)

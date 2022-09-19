from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Category,
    ChildCategory,
    Advertisement,
    AdsSubscriber,
    AdsImage,
    City,
    Subscription,
    AdsComment,
    ComplainingForAds,
    Favorite
)


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_prices', 'child_category', 'created_at', 'modified_at', 'disable_date')
    list_display_links = ('id', 'name')
    list_filter = ('city', 'child_category', 'owner', 'created_at', 'modified_at', 'disable_date')
    search_fields = ('name', 'description', 'email')
    readonly_fields = ('disable_date', 'slug')

    def get_prices(self, obj):
        return f'{obj.price}-{obj.max_price}' if obj.max_price else obj.price

    get_prices.short_description = 'Цена'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_icon')
    list_display_links = ('id', 'name')
    readonly_fields = ('get_icon',)

    def get_icon(self, obj):
        """
        Метод для получение картинки в виде отрендеренного html
        """
        return mark_safe(f'<img src={obj.icon.url} width="150" height="150">') if obj.icon else '-'

    get_icon.short_description = 'Иконка'


@admin.register(ChildCategory)
class ChildCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('category',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_icon')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    readonly_fields = ('get_icon',)

    def get_icon(self, obj):
        """
        Метод для получение картинки в виде отрендеренного html
        """
        return mark_safe(f'<img src={obj.icon.url} width="130" height="180">') if obj.icon else '-'

    get_icon.short_description = 'Иконка'


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


@admin.register(AdsImage)
class AdsImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'advertisement', 'get_image')
    list_display_links = ('id', 'advertisement')
    list_filter = ('advertisement',)
    search_fields = ('advertisement',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        """
        Метод для получение картинки в виде отрендеренного html
        """
        return mark_safe(f'<img src={obj.image.url} width="130" height="180">') if obj.image else '-'

    get_image.short_description = 'Изображение'


@admin.register(AdsComment)
class AdsCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'advertisement', 'created_on', 'modified_at')
    list_filter = ('created_on', 'modified_at', 'user')
    search_fields = ('user', 'text')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('id',)
    list_filter = ('advertisements', 'user')


@admin.register(ComplainingForAds)
class ComplainingForAdsAdmin(admin.ModelAdmin):
    list_display = ('id', 'advertisement', 'type', 'send_date', 'checked_at', 'is_checked')
    list_display_links = ('id', 'advertisement')
    list_filter = ('advertisement', 'type', 'send_date', 'checked_at', 'is_checked')
    search_fields = ('text',)
    readonly_fields = ('checked_at',)
    list_editable = ('type', 'is_checked',)

from django.contrib import admin
from .models import Site, SocialMedia, FeedBack, Help

from django.utils.safestring import mark_safe


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    """
    Админ панель "Информация сайта"
    """
    list_display = ('name', 'logo', 'privacy_policy_text', 'copyright')
    list_display_links = ('name', 'logo')

    def get_site_logo(self, obj):
        return mark_safe(f"<img src={obj.logo.url}>") if obj.logo else '-'

    get_site_logo.short_description = 'Логотип'


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    """
    Админ панель "Информация сайта"
    """
    list_display = ('name', 'image', 'type', 'link')
    list_display_links = ('name', 'image')

    def get_site_logo(self, obj):
        return mark_safe(f"<img src={obj.image.url}>") if obj.image else '-'

    get_site_logo.short_description = 'Изображение'


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    """
    Админ панель "Обратный звонок"
    """
    list_display = ('name', 'email', 'subject', 'send_date', 'check_date', 'checked')
    list_display_links = ('name', 'email')
    readonly_fields = ('send_date', 'check_date')
    search_fields = ('name', 'email')
    list_filter = ('email', 'subject', 'send_date', 'check_date', 'checked')


@admin.register(Help)
class HelpAdmin(admin.ModelAdmin):
    """
    Админ панель "Раздел помощь"
    """
    list_display = ('title', 'text')
    list_display_links = ('title',)

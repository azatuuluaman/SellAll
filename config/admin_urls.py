from django.urls import path, include

from rest_framework.routers import DefaultRouter

from advertisement.views.admin_views import AdminComplainingView, AdvertisementByComplaining
from siteapp.views import FeedBackAdminView

router = DefaultRouter()
router.register(r'complain', AdminComplainingView, basename="complain")

urlpatterns = [
    path('', include(router.urls), name='admin'),
    path('ads-with-complaining/', AdvertisementByComplaining.as_view(), name='ads_with_complaining'),
    path('feedback/', FeedBackAdminView.as_view(), name='admin_feedback'),
]

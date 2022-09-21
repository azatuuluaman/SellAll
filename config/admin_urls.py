from django.urls import path, include

from rest_framework.routers import DefaultRouter

from advertisement.views.admin_views import AdminComplainingView, AdvertisementByComplaining
from advertisement.views.advertisement_views import AdvertisementListView, UserAdvertisementListView, \
    AdvertisementRUDView
from siteapp.views import FeedBackAdminView
from user.views import UsersAPIView, UserAPIView, DeleteUserAPIView

router = DefaultRouter()
router.register(r'complain', AdminComplainingView, basename="complain")

urlpatterns = [
    path('', include(router.urls), name='admin'),
    path('list/', AdvertisementListView.as_view(), name='admin_list'),
    path('<int:pk>/', AdvertisementRUDView.as_view(), name='admin_ads'),
    path('ads-with-complaining/', AdvertisementByComplaining.as_view(), name='ads_with_complaining'),
    path('feedback/', FeedBackAdminView.as_view(), name='admin_feedback'),
    path('users/', UsersAPIView.as_view(), name='admin_user_list'),
    path('user/', UserAPIView.as_view(), name='admin_user'),
    path('delele-user/', DeleteUserAPIView.as_view(), name='admin_delete_user')
]

from django.urls import path, include

from rest_framework import routers

from advertisement.views import AdvertisementAPIView
from user.views import RegisterUserView, ActivationView

router = routers.DefaultRouter()
router.register('advertisement', AdvertisementAPIView)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('siteapp.urls')),
    path('', include('advertisement.urls')),
]

urlpatterns_auth = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('activation/<str:code>/', ActivationView.as_view(), name='activate'),
]

urlpatterns += urlpatterns_auth

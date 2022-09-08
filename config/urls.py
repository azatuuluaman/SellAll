"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView

from advertisement.views import AdvertisementAPIView
from user.views import RegisterUserView, ActivationView
from .swagger_config import urlpatterns as swg


router = routers.DefaultRouter()
router.register('advertisement', AdvertisementAPIView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='verify'),
    path('api/logout/', TokenBlacklistView.as_view(), name='logout'),

    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/activation/<str:code>/', ActivationView.as_view(), name='activate'),

    path('api/', include(router.urls), name='api'),
    path('api/', include('siteapp.urls')),
    path('api/', include('advertisement.urls')),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += swg

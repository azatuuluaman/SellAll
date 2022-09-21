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

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from .swagger_config import urlpatterns as swg
from .admin_urls import urlpatterns as admin_url

API_HEAD_URL = f'api/v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),

    path(f'{API_HEAD_URL}/social-auth/', include('social_auth.urls'), name='social'),
    path(f'{API_HEAD_URL}/token/', TokenObtainPairView.as_view(), name='login'),
    path(f'{API_HEAD_URL}/token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path(f'{API_HEAD_URL}/logout/', TokenBlacklistView.as_view(), name='logout'),

    path(f'{API_HEAD_URL}/user/', include('user.urls')),
    path(f'{API_HEAD_URL}/site/', include('siteapp.urls')),
    path(f'{API_HEAD_URL}/advertisement/', include('advertisement.urls')),
    path(f'{API_HEAD_URL}/chat/', include('chat.urls')),
    path(f'{API_HEAD_URL}/admin/', include(admin_url))
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += swg

from django.urls import path

from .views import RegisterUserView, UserActivationView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('activation/', UserActivationView.as_view(), name='activate'),
]

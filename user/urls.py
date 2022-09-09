from django.urls import path

from .views import RegisterUserView, ActivationView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('activation/<str:code>/', ActivationView.as_view(), name='activate'),
]

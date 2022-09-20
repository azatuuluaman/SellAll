from django.urls import path

from .views import (
    RegisterUserView,
    UserActivationView,
    UserAPIView,
    SendMassAPIView,
    ForgotPasswordAPIView,
)

urlpatterns = [
    path('', UserAPIView.as_view(), name='user'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('activation/', UserActivationView.as_view(), name='activate'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('send-mass/', SendMassAPIView.as_view(), name='send_mass'),
]

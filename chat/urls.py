from django.urls import path

from chat.views import MessageAPIView

urlpatterns = [
    path('message/', MessageAPIView.as_view(), name='message')
]
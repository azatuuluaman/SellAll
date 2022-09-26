from django.urls import path

from .views import OrderPaymentListView, OrderPaymentAPIView

urlpatterns = [
    path("list/", OrderPaymentListView.as_view()),
    path("payment/", OrderPaymentAPIView.as_view()),
]
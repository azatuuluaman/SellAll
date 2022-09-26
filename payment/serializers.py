from rest_framework import serializers

from .models import OrderPayment


class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = ["advertisement", "user_name", "description", "amount"]

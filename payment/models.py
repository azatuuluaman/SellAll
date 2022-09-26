from django.db import models

from advertisement.models import Advertisement


class OrderPayment(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.SET_NULL, null=True)
    user_name = models.CharField("Имя пользователя", max_length=50)
    description = models.TextField("Описание")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    amount = models.PositiveIntegerField("Сумма с сомах")
    is_paid = models.BooleanField("Оплачено", default=False)

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

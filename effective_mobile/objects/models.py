from django.db import models

from users.models import User


class Product(models.Model):
    """Таблица продуктов"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Order(models.Model):
    """Таблица заказов"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Order {self.id} - {self.product.name}"
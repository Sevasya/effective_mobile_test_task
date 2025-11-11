from rest_framework import serializers
from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор продуктов"""
    class Meta:
        model = Product
        fields = ['id', 'name']


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор заказов"""
    class Meta:
        model = Order
        fields = ['id', 'product', 'owner', 'quantity']
from django.core.management.base import BaseCommand

from users.models import User
from objects.models import Product, Order


class Command(BaseCommand):
    help = "Создает бизнес-объекты и элементы для демонстрации RBAC"

    def handle(self, *args, **options):
        self.stdout.write("Созданы BusinessElement: products, orders")

        admin = User.objects.filter(email="admin@example.com").first()
        user1 = User.objects.filter(email="user1@example.com").first()
        user2 = User.objects.filter(email="user2@example.com").first()

        if not all([admin, user1, user2]):
            self.stdout.write(self.style.ERROR("Пользователи не найдены! Сначала создайте их командой init_rbac."))
            return

        products = [
            {"name": "Laptop"},
            {"name": "Phone"},
            {"name": "Tablet"},
        ]
        for p in products:
            Product.objects.get_or_create(name=p["name"])

        self.stdout.write("Созданы тестовые продукты")

        orders = [
            {"product_name": "Laptop", "owner": user1, "quantity": 2},
            {"product_name": "Phone", "owner": user2, "quantity": 1},
        ]
        for o in orders:
            product = Product.objects.get(name=o["product_name"])
            Order.objects.get_or_create(product=product, owner=o["owner"], quantity=o["quantity"])

        self.stdout.write(self.style.SUCCESS("Созданы тестовые заказы"))

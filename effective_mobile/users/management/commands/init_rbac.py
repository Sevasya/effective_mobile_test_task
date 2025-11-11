from django.core.management.base import BaseCommand
from users.models import Role, AccessRoleRule, User


class Command(BaseCommand):
    help = "Создает начальные роли, объекты, правила доступа и тестовых пользователей"

    def handle(self, *args, **options):
        self.stdout.write("Создаем роли...")
        admin_role, _ = Role.objects.get_or_create(name="admin")
        user_role, _ = Role.objects.get_or_create(name="user")

        self.stdout.write("Создаем правила доступа...")

        AccessRoleRule.objects.get_or_create(
            role=admin_role,
            read_exact_permission=True, read_all_permission=True,
        )
        AccessRoleRule.objects.get_or_create(
            role=user_role, 
            read_exact_permission=True, read_all_permission=True,
        )

        self.stdout.write("Создаем пользователей...")

        users_data = [
            {"email": "admin@example.com", "first_name": "Admin", "last_name": "User", "role": admin_role, "password": "admin123"},
            {"email": "user1@example.com", "first_name": "User1", "last_name": "Test", "role": user_role, "password": "user123"},
            {"email": "user2@example.com", "first_name": "User2", "last_name": "Test", "role": user_role, "password": "user123"},
        ]

        for udata in users_data:
            user, created = User.objects.get_or_create(email=udata["email"], defaults={
                "first_name": udata["first_name"],
                "last_name": udata["last_name"],
                "role": udata["role"]
            })
            user.set_password(udata["password"])
            user.save()
            if created:
                self.stdout.write(f"Создан пользователь: {udata['email']}")
            else:
                self.stdout.write(f"Пользователь уже существует: {udata['email']}")

        self.stdout.write(self.style.SUCCESS("RBAC таблицы, правила и тестовые пользователи созданы!"))

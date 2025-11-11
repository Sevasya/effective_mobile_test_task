import bcrypt
from django.db import models
from django.utils import timezone


class Role(models.Model):
    """Таблица ролей"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(models.Model):
    """Таблица пользователей"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def set_password(self, raw_password: str):
        """Хеширование пароля"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
        self.password_hash = hashed.decode('utf-8')
        self.save()

    def check_password(self, raw_password: str):
        """Проверка пароля на совпадение с паролем в БД"""
        if not self.password_hash:
            return False
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def soft_delete(self):
        """Мягкое удаление"""
        self.is_active = False
        self.save()
    

class AccessRoleRule(models.Model):
    """
    Таблица прав доступа - изначально все могут просматировать конкретный продукт и все продукты
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="rules")

    read_all_permission = models.BooleanField(default=True)
    read_exact_permission = models.BooleanField(default=True)

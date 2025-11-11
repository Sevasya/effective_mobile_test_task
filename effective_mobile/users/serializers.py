from rest_framework import serializers
from users.models import User, AccessRoleRule


class EmptySerializer(serializers.Serializer):
    """Сериализатор заглушка"""
    pass


class RoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRoleRule
        exclude = ['id', 'role']


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя"""
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        exclude = ['id', 'password_hash', 'is_active']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data
    
    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            middle_name=validated_data['middle_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        return user
    

class UserLoginSerializer(serializers.Serializer):
    """Сериализатор логина пользователя"""
    email = serializers.EmailField()
    password = serializers.CharField()


class UserDetailSerializer(serializers.ModelSerializer):
    """Сериализатор информаии о пользователе"""
    class Meta:
        model = User
        exclude = ['password_hash']


class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор обновления пользователя"""
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name']

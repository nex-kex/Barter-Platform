from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserCreationSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/регистрации пользователя."""

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]

    def validate_password(self, password):
        validate_password(password)
        return password


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра пользователя."""

    id = serializers.IntegerField(read_only=True)
    date_joined = serializers.DateField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "date_joined"]

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import UserCreationSerializer, UserSerializer
from .permissions import IsUser
from .models import User


class UserCreateView(generics.CreateAPIView):
    """Класс для создания пользователя."""

    serializer_class = UserCreationSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveView(generics.RetrieveAPIView):
    """Класс для получения информации об определённом пользователе."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(generics.UpdateAPIView):
    """Класс для обновления пользователя."""

    queryset = User.objects.all()
    serializer_class = UserCreationSerializer
    permission_classes = [IsUser, IsAuthenticated]

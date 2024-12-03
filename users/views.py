from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from .models import CustomUser
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAdminUser
    ]  # Только администраторы могут управлять пользователями

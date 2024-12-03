from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import NetworkElement, Product
from .permissions import (IsAdminOnlyForDelete, IsAdminOrReadOnly,
                          IsManagerOrAdmin)
from .serializers import NetworkElementSerializer, ProductSerializer


class NetworkElementViewSet(ModelViewSet):
    queryset = NetworkElement.objects.all()
    serializer_class = NetworkElementSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]  # Фильтрация по стране

    def create(self, request, *args, **kwargs):
        """Создание элемента сети с отладочными выводами."""
        print(f"DEBUG: Raw Request data: {request.data}")  # Отладка
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ["destroy"]:
            return [IsAdminOnlyForDelete()]  # Только администраторы могут удалять
        if self.action in ["create", "update", "partial_update"]:
            return [IsManagerOrAdmin()]  # Менеджеры и администраторы могут изменять
        return [IsAdminOrReadOnly()]  # Только чтение для сотрудников

    @extend_schema(
        description="Обновление элемента сети. Поле 'debt' недоступно для изменения.",
        responses={400: {"description": "Поле 'debt' нельзя изменять через API."}},
        parameters=[
            OpenApiParameter(
                name="country",
                description="Фильтр по стране (например, Россия)",
                required=False,
                type=str,
            )
        ],
    )
    def update(self, request, *args, **kwargs):
        if "debt" in request.data:
            return Response(
                {"detail": "Поле 'debt' нельзя изменять через API."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        country = self.request.query_params.get("country")
        if country:
            queryset = queryset.filter(country=country).exclude(
                level=2
            )  # Исключаем сотрудников
        return queryset

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ["destroy"]:
            return [IsAdminOnlyForDelete()]  # Только администраторы могут удалять
        if self.action in ["create", "update", "partial_update"]:
            return [IsManagerOrAdmin()]  # Менеджеры и администраторы могут изменять
        return [IsAdminOrReadOnly()]  # Только чтение для сотрудников

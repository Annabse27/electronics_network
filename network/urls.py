from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import NetworkElementViewSet, ProductViewSet

router = DefaultRouter()
router.register("network", NetworkElementViewSet)
router.register("product", ProductViewSet)

# Добавляем маршруты роутера
urlpatterns = [
    path("", include(router.urls)),  # Включаем маршруты DefaultRouter
]

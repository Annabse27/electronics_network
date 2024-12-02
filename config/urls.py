from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path("admin/", admin.site.urls),  # Админка
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # JWT токены
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # Обновление токена
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),  # Схема OpenAPI
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),  # Swagger UI
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui-schema",
    ),
    path(
        "api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),  # Альтернативная документация
    path("api/network/", include("network.urls")),  # Эндпоинты приложения network
    path("api/", include("users.urls")),
]

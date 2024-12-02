from rest_framework.permissions import BasePermission


class IsActivePermission(BasePermission):
    """
    Разрешение, которое позволяет доступ только активным пользователям.
    """

    def has_permission(self, request, view):
        return (
            request.user and request.user.is_active
        )  # Проверяем, что пользователь активен


class IsAdminOrReadOnly(BasePermission):
    """
    Разрешение: Администраторы имеют полный доступ, остальные только чтение.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == "admin":  # Полный доступ для администраторов
                return True
            # Остальные роли только для чтения
            return request.method in ["GET", "HEAD", "OPTIONS"]
        return False


class IsManagerOrAdmin(BasePermission):
    """
    Разрешение: Менеджеры и администраторы имеют доступ на чтение/создание/изменение.
    Сотрудники только на чтение.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role in ["admin", "manager"]:  # Менеджеры и администраторы
                return True
            # Сотрудники только для чтения
            return request.method in ["GET", "HEAD", "OPTIONS"]
        return False


class IsAdminOnlyForDelete(BasePermission):
    """
    Разрешение: только администраторы могут удалять.
    """

    def has_permission(self, request, view):
        if request.method == "DELETE":
            return request.user.is_authenticated and request.user.role == "admin"
        return True  # Другие методы проверяются в основном разрешении

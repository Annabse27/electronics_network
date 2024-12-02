from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from .models import NetworkElement, Product


@admin.register(NetworkElement)
class NetworkElementAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "city", "country", "debt", "supplier_link")
    search_fields = ("name", "city", "country", "email", "phone")
    list_filter = ("city", "country", "level")
    actions = ["clear_debt"]

    def get_form(self, request, obj=None, **kwargs):
        """
        Отключаем поле 'Поставщик' для Заводов (уровень 0).
        """
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.level == 0:
            form.base_fields["supplier"].disabled = True  # Делаем поле неактивным
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Ограничиваем доступные варианты для поля 'Поставщик'
        в зависимости от уровня элемента сети.
        """
        if db_field.name == "supplier":
            # Получаем текущий объект (если он редактируется)
            obj_id = request.resolver_match.kwargs.get("object_id")
            if obj_id:
                current_object = NetworkElement.objects.get(id=obj_id)
                if current_object.level == 1:
                    # Уровень 1 может иметь поставщиков уровня 0
                    kwargs["queryset"] = NetworkElement.objects.filter(level=0)
                elif current_object.level == 2:
                    # Уровень 2 может иметь поставщиков уровня 1
                    kwargs["queryset"] = NetworkElement.objects.filter(level=1)
            else:
                # Если создается новый объект, оставляем стандартный queryset
                kwargs["queryset"] = NetworkElement.objects.none()  # Пустой список
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def clear_debt(self, request, queryset):
        """
        Admin action для обнуления задолженности.
        """
        queryset.update(debt=0.0)
        self.message_user(
            request, f"Задолженность успешно обнулена у {queryset.count()} объектов."
        )

    clear_debt.short_description = "Очистить задолженность"

    def supplier_link(self, obj):
        """
        Генерирует ссылку на поставщика, если он существует.
        """
        if obj.supplier:
            return format_html(
                '<a href="/admin/network/networkelement/{}/change/">{}</a>',
                obj.supplier.id,
                obj.supplier.name,
            )
        return "Нет поставщика"

    supplier_link.short_description = "Поставщик"

    def save_model(self, request, obj, form, change):
        """
        Проверяет уникальность элемента сети по имени и уровню при сохранении.
        """
        obj.clean()  # Вызываем метод clean из модели
        super().save_model(request, obj, form, change)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "model",
        "release_date",
        "price",
        "manufacturer_country",
        "network_element",
    )
    search_fields = ("name", "model", "manufacturer_country")
    list_filter = ("release_date", "manufacturer_country", "network_element")

    def save_model(self, request, obj, form, change):
        """
        Проверяет уникальность продукта по названию, модели и элементу сети.
        """
        if (
            not change
            and Product.objects.filter(
                name=obj.name, model=obj.model, network_element=obj.network_element
            ).exists()
        ):
            raise ValidationError(
                "Продукт с таким названием, моделью и элементом сети уже существует."
            )
        super().save_model(request, obj, form, change)

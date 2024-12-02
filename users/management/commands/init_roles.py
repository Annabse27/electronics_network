from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from network.models import NetworkElement, Product


class Command(BaseCommand):
    help = "Инициализация ролей и прав"

    def handle(self, *args, **kwargs):
        # Создание групп
        admin_group, _ = Group.objects.get_or_create(name="Администраторы")
        manager_group, _ = Group.objects.get_or_create(name="Менеджеры")
        employee_group, _ = Group.objects.get_or_create(name="Сотрудники")

        # Права для NetworkElement и Product
        network_ct = ContentType.objects.get_for_model(NetworkElement)
        product_ct = ContentType.objects.get_for_model(Product)

        # Администратор: все права
        admin_group.permissions.set(
            Permission.objects.filter(content_type__in=[network_ct, product_ct])
        )

        # Менеджер: просмотр, добавление, изменение
        manager_group.permissions.set(
            Permission.objects.filter(
                content_type__in=[network_ct, product_ct],
                codename__in=[
                    "view_networkelement",
                    "add_networkelement",
                    "change_networkelement",
                    "view_product",
                    "add_product",
                    "change_product",
                ],
            )
        )

        # Сотрудник: только просмотр
        employee_group.permissions.set(
            Permission.objects.filter(
                content_type__in=[network_ct, product_ct],
                codename__in=["view_networkelement", "view_product"],
            )
        )

        self.stdout.write(self.style.SUCCESS("Роли и права успешно инициализированы!"))

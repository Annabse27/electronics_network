from django.core.exceptions import ValidationError
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    model = models.CharField(max_length=100, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода на рынок")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена (₽)"
    )
    manufacturer_country = models.CharField(
        max_length=100, verbose_name="Страна производителя"
    )
    network_element = models.ForeignKey(
        "NetworkElement",
        on_delete=models.CASCADE,
        related_name="product_list",
        verbose_name="Связанное звено сети",
    )

    class Meta:
        unique_together = ("name", "model")  # Уникальная пара (название + модель)
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} ({self.model})"


class NetworkElement(models.Model):
    LEVELS = (
        (0, "Завод"),
        (1, "Розничная сеть"),
        (2, "Индивидуальный предприниматель"),
    )

    level = models.IntegerField(choices=LEVELS, verbose_name="Уровень сети")
    name = models.CharField(max_length=255, verbose_name="Название")
    email = models.EmailField(verbose_name="Электронная почта", unique=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", unique=True)
    inn = models.CharField(max_length=12, verbose_name="ИНН", blank=True, null=True)
    kpp = models.CharField(max_length=9, verbose_name="КПП", blank=True, null=True)
    country = models.CharField(max_length=100, default="Россия", verbose_name="Страна")
    region = models.CharField(max_length=100, verbose_name="Регион")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=10, verbose_name="Номер дома")
    postal_code = models.CharField(max_length=6, verbose_name="Почтовый индекс")
    supplier = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="clients",
        verbose_name="Поставщик",
    )
    debt = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, verbose_name="Задолженность (₽)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def clean(self):
        """
        Проверка уровня поставщика.
        """
        if self.level == 0 and self.supplier:
            raise ValidationError("Завод (уровень 0) не может иметь поставщика.")
        if self.level == 1 and (not self.supplier or self.supplier.level != 0):
            raise ValidationError(
                "Розничная сеть (уровень 1) должна иметь поставщика уровня 0 (Завод)."
            )
        if self.level == 2 and (not self.supplier or self.supplier.level != 1):
            raise ValidationError(
                "Индивидуальный предприниматель (уровень 2) должен иметь поставщика уровня 1 (Розничная сеть)."
            )

    def save(self, *args, **kwargs):
        self.clean()  # Вызываем валидацию перед сохранением
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("name", "level")  # Уникальная пара (название + уровень)
        verbose_name = "Элемент сети"
        verbose_name_plural = "Элементы сети"

    def __str__(self):
        return self.name

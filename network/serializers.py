from rest_framework import serializers

from network.models import NetworkElement, Product


class ProductSerializer(serializers.ModelSerializer):
    название = serializers.CharField(source="name", label="Название")
    модель = serializers.CharField(source="model", label="Модель")
    дата_выхода = serializers.DateField(
        source="release_date", label="Дата выхода на рынок"
    )
    цена = serializers.DecimalField(
        source="price", max_digits=10, decimal_places=2, label="Цена (₽)"
    )
    страна_производителя = serializers.CharField(
        source="manufacturer_country", label="Страна производителя"
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "название",
            "модель",
            "дата_выхода",
            "цена",
            "страна_производителя",
        ]


class NetworkElementSerializer(serializers.ModelSerializer):
    продукты = ProductSerializer(
        source="product_list", many=True, read_only=True, label="Продукты"
    )
    уровень_сети = serializers.IntegerField(source="level", label="Уровень сети")
    название = serializers.CharField(source="name", label="Название")
    электронная_почта = serializers.EmailField(
        source="email", label="Электронная почта"
    )
    телефон = serializers.CharField(source="phone", label="Телефон")
    страна = serializers.CharField(source="country", label="Страна")
    регион = serializers.CharField(source="region", label="Регион")
    город = serializers.CharField(source="city", label="Город")
    улица = serializers.CharField(source="street", label="Улица")
    номер_дома = serializers.CharField(source="house_number", label="Номер дома")
    почтовый_индекс = serializers.CharField(
        source="postal_code", label="Почтовый индекс"
    )
    задолженность = serializers.DecimalField(
        source="debt",
        max_digits=10,
        decimal_places=2,
        read_only=True,
        label="Задолженность",
    )
    создано = serializers.DateTimeField(
        source="created_at", read_only=True, label="Создано"
    )
    # Обновляем поле `поставщик`
    поставщик = serializers.PrimaryKeyRelatedField(
        queryset=NetworkElement.objects.all(),  # Разрешить всех поставщиков        required=False,
        required=False,
        allow_null=True,
        label="ID поставщика",
    )

    class Meta:
        model = NetworkElement
        fields = [
            "id",  # ID элемента сети
            "уровень_сети",
            "название",
            "электронная_почта",
            "телефон",
            "страна",
            "регион",
            "город",
            "улица",
            "номер_дома",
            "почтовый_индекс",
            "задолженность",
            "создано",
            "поставщик",
            "продукты",  # Продукты связаны с элементом сети
        ]

    def create(self, validated_data):
        # Переименовываем поле "поставщик" в "supplier"
        supplier = validated_data.pop("поставщик", None)
        validated_data["supplier"] = supplier
        return super().create(validated_data)

    def update(self, instance, validated_data):
        supplier = validated_data.pop("поставщик", None)
        validated_data["supplier"] = supplier
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """
        Переопределяем представление для поля `поставщик`.
        """
        representation = super().to_representation(instance)
        if instance.supplier:  # Если у элемента есть поставщик
            representation["поставщик"] = {
                "id": instance.supplier.id,
                "название": instance.supplier.name,
                "уровень_сети": instance.supplier.get_level_display(),
            }
        else:
            representation["поставщик"] = None
        return representation

    def get_поставщик(self, obj):
        """
        Возвращает информацию о поставщике.
        """
        if obj.supplier:
            return {
                "id": obj.supplier.id,
                "название": obj.supplier.name,
                "уровень_сети": obj.supplier.get_level_display(),
            }
        return None

    def validate(self, data):
        level = data.get("level")
        supplier = data.get("supplier")

        if level is None:
            raise serializers.ValidationError({"уровень_сети": "Это поле обязательно."})

        # Проверяем корректность уровня поставщика
        if supplier:
            if level == 1 and supplier.level != 0:
                raise serializers.ValidationError(
                    "Розничная сеть (уровень 1) должна иметь поставщика уровня 0 (Завод)."
                )
            if level == 2 and supplier.level != 1:
                raise serializers.ValidationError(
                    "Индивидуальный предприниматель (уровень 2) должен иметь поставщика уровня 1 (Розничная сеть)."
                )

        if level == 0 and supplier:
            raise serializers.ValidationError(
                "Завод (уровень 0) не может иметь поставщика."
            )

        # Проверка уникальности на уровне модели

        if NetworkElement.objects.filter(name=data["name"], level=level).exists():
            raise serializers.ValidationError(
                "Элемент сети с таким названием и уровнем уже существует."
            )

        instance_id = self.instance.id if self.instance else None
        if "email" in data:
            if (
                NetworkElement.objects.filter(email=data["email"])
                .exclude(id=instance_id)
                .exists()
            ):
                raise serializers.ValidationError(
                    {"email": "Элемент сети с таким email уже существует."}
                )

        if "phone" in data:
            if (
                NetworkElement.objects.filter(phone=data["phone"])
                .exclude(id=instance_id)
                .exists()
            ):
                raise serializers.ValidationError(
                    {"phone": "Элемент сети с таким телефоном уже существует."}
                )

        # Нельзя изменять задолженность через АПИ
        if "debt" in self.initial_data:
            raise serializers.ValidationError(
                {"detail": "Поле 'debt' нельзя изменять через API."}
            )

        # Добавляем supplier в данные для создания объекта
        data["level"] = int(level)
        data["supplier"] = supplier

        return data

import pytest
from rest_framework.test import APIClient

from network.models import NetworkElement, Product
from network.serializers import NetworkElementSerializer, ProductSerializer


# для сериализаторов
@pytest.mark.django_db
def test_network_element_serializer():
    factory = NetworkElement.objects.create(
        level=0,
        name="Завод Электроника",
        email="factory@example.com",
        phone="1234567890",
        country="Россия",
        region="Московская область",
        city="Москва",
        street="Ленина",
        house_number="10",
        postal_code="123456",
        debt=0.0,
    )
    serializer = NetworkElementSerializer(instance=factory)
    data = serializer.data

    assert data["название"] == "Завод Электроника"
    assert data["уровень_сети"] == 0  # Числовое значение из сериализатора
    assert factory.get_level_display() == "Завод"  # Текстовое представление из модели


@pytest.mark.django_db
def test_product_serializer():
    factory = NetworkElement.objects.create(
        level=0,
        name="Завод Электроника",
        email="factory@example.com",
        phone="1234567890",
    )
    product = Product.objects.create(
        name="Смартфон X1",
        model="X1-2024",
        release_date="2024-01-15",
        price=20000.0,
        manufacturer_country="Россия",
        network_element=factory,
    )
    serializer = ProductSerializer(instance=product)
    data = serializer.data
    assert data["название"] == "Смартфон X1"
    assert data["модель"] == "X1-2024"

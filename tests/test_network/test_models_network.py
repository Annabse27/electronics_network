import pytest

from network.models import NetworkElement, Product


@pytest.mark.django_db
def test_network_element_creation():
    """Тест создания элемента сети."""
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
    )
    assert factory.name == "Завод Электроника"
    assert factory.level == 0


@pytest.mark.django_db
def test_product_creation():
    """Тест создания продукта."""
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
    )
    product = Product.objects.create(
        name="Смартфон X1",
        model="X1-2024",
        release_date="2024-01-15",
        price=20000.0,
        manufacturer_country="Россия",
        network_element=factory,
    )
    assert product.name == "Смартфон X1"
    assert product.network_element == factory

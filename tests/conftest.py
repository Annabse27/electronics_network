import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from network.models import NetworkElement, Product


@pytest.fixture
def api_client():
    """Фикстура для API-клиента."""
    return APIClient()


@pytest.fixture
def create_user():
    def make_user(**kwargs):
        User = get_user_model()
        user = User.objects.create_user(**kwargs)
        return user

    return make_user


@pytest.fixture
def manager_user(create_user):
    return create_user(username="manager", password="manager123", role="manager")


@pytest.fixture
def setup_data():
    """
    Создаёт тестовые данные для NetworkElement и Product.
    """
    factory = NetworkElement.objects.create(
        level=0,
        name="Тестовый завод",
        email="factory@example.com",
        phone="1234567890",
        country="Россия",
        region="Московская область",
        city="Москва",
        street="Тестовая улица",
        house_number="1",
        postal_code="123456",
        debt=0.0,
    )
    retail_network = NetworkElement.objects.create(
        level=1,
        name="Тестовая сеть",
        email="retail@example.com",
        phone="0987654321",
        country="Россия",
        region="Санкт-Петербург",
        city="Санкт-Петербург",
        street="Другая улица",
        house_number="2",
        postal_code="654321",
        supplier=factory,
        debt=10000.0,
    )
    product = Product.objects.create(
        name="Тестовый продукт",
        model="TP-2024",
        release_date="2024-01-01",
        price=50000.0,
        manufacturer_country="Россия",
        network_element=factory,
    )
    return {"factory": factory, "retail_network": retail_network, "product": product}


@pytest.fixture
def get_token(api_client, create_user):
    """Фикстура для получения токена аутентификации."""
    user = create_user(username="manager", password="manager123", role="manager")
    response = api_client.post(
        "/api/token/",
        {"username": "manager", "password": "manager123"},
        format="json",
    )
    assert response.status_code == 200, f"Ошибка получения токена: {response.data}"
    return response.data["access"]

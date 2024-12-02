import pytest

from network.models import NetworkElement


@pytest.mark.django_db
def test_get_network_elements(api_client, get_token, setup_data):
    """Тест получения списка элементов сети."""
    token = get_token
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = api_client.get("/api/network/")
    assert response.status_code == 200, f"Ошибка: {response.data}"


@pytest.mark.django_db
def test_create_network_element(api_client, manager_user, setup_data):
    api_client.force_authenticate(user=manager_user)

    # Указание существующего поставщика уровня 0
    factory = setup_data["factory"]  # Завод из фикстуры

    data = {
        "название": "Новая сеть",
        "электронная_почта": "new@network.com",
        "телефон": "1234567880",
        "страна": "Россия",
        "регион": "Москва",
        "город": "Москва",
        "улица": "Ленина",
        "номер_дома": "1",
        "почтовый_индекс": "919991",
        "уровень_сети": 1,
        "поставщик": factory.id,  # Указываем ID завода
    }

    response = api_client.post("/api/network/network/", data, format="json")
    assert response.status_code == 201, f"Ошибка: {response.data}"

import pytest
from rest_framework.test import APIClient

from users.models import CustomUser


# для моделей
@pytest.mark.django_db
def test_user_creation():
    user = CustomUser.objects.create_user(
        username="test_user", password="password123", role="manager"
    )
    assert user.role == "manager"
    assert user.check_password("password123")


# для АПИ
@pytest.mark.django_db
def test_get_users(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    response = client.get("/api/users/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    data = {
        "username": "new_user",
        "email": "new_user@example.com",
        "password": "securepassword",
        "role": "employee",
    }
    response = client.post("/api/users/", data, format="json")
    assert response.status_code == 201
    assert CustomUser.objects.filter(username="new_user").exists()

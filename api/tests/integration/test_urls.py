import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_should_configure_categories_api():
    response = APIClient().get("/api/v1/categories/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_should_configure_ingredients_api():
    response = APIClient().get("/api/v1/ingredients/")
    assert response.status_code == 200

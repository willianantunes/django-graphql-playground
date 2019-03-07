import pytest
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from graphqlclient import GraphQLClient
from rest_framework.test import APIClient

from api.models import Category, Ingredient


@pytest.fixture
def prepare_db():
    fake_category_name = "fake-category-name"
    fake_category = Category.objects.create(name=fake_category_name)
    fake_ingredient_notes = "fake_ingredient_notes"
    fake_ingredient_name = "fake_ingredient_name"
    Ingredient.objects.create(name=fake_ingredient_name, notes=fake_ingredient_notes, category=fake_category)


@pytest.mark.django_db
def test_should_configure_categories_api():
    response = APIClient().get("/api/v1/categories/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_should_configure_ingredients_api():
    response = APIClient().get("/api/v1/ingredients/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_prisma_python_graphql_client(live_server):
    """
    Know more at: https://github.com/prisma/python-graphql-client
    """

    client = GraphQLClient(f"{live_server.url}/api/graphql/")
    query = """
        query {
          allCategories{
            id
            name
            ingredients {
              id
              name
              notes
            }
          }
        }
    """
    result = client.execute(query)

    assert result == "{'data':{'allCategories':[]}}"


@pytest.mark.django_db
def test_gql_client(live_server, prepare_db):
    """
    Know more at: https://github.com/graphql-python/gql
    """

    transport = RequestsHTTPTransport(f"{live_server.url}/api/graphql/")
    client = Client(transport=transport)

    query = gql(
        """
        query {
          allCategories{
            id
            name
            ingredients {
              id
              name
              notes
            }
          }
        }
    """
    )
    result = client.execute(query)

    assert len(result["allCategories"]) == 1
    for category in result["allCategories"]:
        assert category["id"] == "1"
        assert category["name"] == "fake-category-name"
        assert len(category["ingredients"]) == 1
        for ingredient in category["ingredients"]:
            assert ingredient["id"] == "1"
            assert ingredient["name"] == "fake_ingredient_name"
            assert ingredient["notes"] == "fake_ingredient_notes"

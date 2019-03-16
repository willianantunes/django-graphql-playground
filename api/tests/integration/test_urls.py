import json

import pytest
import requests
from django.contrib.auth import get_user_model
from gql import Client
from gql import gql
from gql.transport.requests import RequestsHTTPTransport
from graphqlclient import GraphQLClient
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.models import Category
from api.models import Ingredient


@pytest.fixture
def prepare_db():
    fake_category_name = "fake-category-name"
    fake_category = Category.objects.create(name=fake_category_name)
    fake_ingredient_notes = "fake_ingredient_notes"
    fake_ingredient_name = "fake_ingredient_name"
    Ingredient.objects.create(name=fake_ingredient_name, notes=fake_ingredient_notes, category=fake_category)


@pytest.mark.django_db
def test_should_get_401_as_categories_api_is_protected():
    response = APIClient().get("/api/v1/categories/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_should_get_401_as_ingredients_api_is_protected():
    response = APIClient().get("/api/v1/ingredients/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_should_generate_token_from_registered_user():
    get_user_model().objects.create_superuser("fake-api-user", None, "fake-api-password")
    data = {"username": "fake-api-user", "password": "fake-api-password"}

    response = APIClient().post("/api/auth-token/", json.dumps(data), content_type="application/json")

    assert response.status_code == 200
    assert type(response.data["token"]) == str
    assert len(response.data["token"]) == 40


def test_should_acess_categories_api_with_authenticated_user(live_server):
    salt_api_user = get_user_model().objects.create_superuser("salt-api-user", None, "salt-api-password")
    created_token = Token.objects.create(key="22216a91b7ddbd7331f0b0ed3af085412f2729de", user=salt_api_user)

    headers = {"Authorization": f"Token {created_token.key}", "Content-Type": "application/json"}
    response = requests.get(f"{live_server.url}/api/v1/categories/", headers=headers)

    assert response.status_code == 200

    headers = {"Content-Type": "application/json"}
    response = requests.get(f"{live_server.url}/api/v1/categories/", headers=headers)

    assert response.status_code == 401


def test_should_authenticate_with_basic_authentication(live_server):
    get_user_model().objects.create_superuser("ant-api-user", None, "ant-api-password")

    session = requests.Session()
    session.auth = ("ant-api-user", "ant-api-password")

    response = session.get(f"{live_server.url}/api/v1/categories/")

    assert response.status_code == 200
    assert requests.get(f"{live_server.url}/api/v1/categories/").status_code == 401


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

    assert result == '{"data":{"allCategories":[]}}'


@pytest.mark.skip(reason="Apparently no way of currently testing this")
def test_gql_client(live_server, prepare_db):
    """
    Know more at: https://github.com/graphql-python/gql
    """

    transport = RequestsHTTPTransport(url=f"{live_server.url}/api/graphql/", use_json=True)
    client = Client(retries=3, transport=transport, fetch_schema_from_transport=True)

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

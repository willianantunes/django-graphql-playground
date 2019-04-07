import json
from urllib.error import HTTPError

import pytest
import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from gql import Client
from gql import gql
from gql.transport.requests import RequestsHTTPTransport
from graphqlclient import GraphQLClient
from requests.auth import HTTPBasicAuth
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from app.models import Category
from app.models import Ingredient


@pytest.fixture
def prepare_db():
    fake_category_name = "fake-category-name"
    fake_category = Category.objects.create(name=fake_category_name)
    fake_ingredient_notes = "fake_ingredient_notes"
    fake_ingredient_name = "fake_ingredient_name"
    Ingredient.objects.create(name=fake_ingredient_name, notes=fake_ingredient_notes, category=fake_category)


@pytest.fixture
def get_user_from_admin():
    User: UserManager = get_user_model().objects
    some_user = User.all().first()
    return some_user if some_user else User.create_superuser("random-user", None, "random-password")


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


def test_prisma_python_graphql_client(live_server, get_user_from_admin):
    """
    Know more at: https://github.com/prisma/python-graphql-client
    """

    some_user = get_user_from_admin
    created_token = Token.objects.create(key="6c5d69c150b32dcb9c746672c0185d6d8454ca21", user=some_user)
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
    try:
        client.execute(query)
    except Exception as e:
        assert type(e) == HTTPError
        assert e.code == 401

    client.inject_token(f"Token {created_token}")
    result = client.execute(query)

    assert result == '{"data":{"allCategories":[]}}'


@pytest.mark.skip(reason="Apparently no way of currently testing this")
def test_gql_client(live_server, prepare_db, get_user_from_admin):
    """
    Know more at: https://github.com/graphql-python/gql
    """

    url = f"{live_server.url}/api/graphql/"
    transport = RequestsHTTPTransport(url=url, use_json=True)
    try:
        Client(retries=3, transport=transport, fetch_schema_from_transport=True)
    except Exception as e:
        assert type(e) == requests.exceptions.HTTPError
        assert e.response.status_code == 401

    some_user = get_user_from_admin
    created_token = Token.objects.create(key="7c5d69c150b32dcb9c746672c0185d6d8454ca21", user=some_user)

    # One way to authenticate
    headers = {"Authorization": f"Token {created_token}"}
    transport = RequestsHTTPTransport(url=url, use_json=True, headers=headers)
    Client(retries=3, transport=transport, fetch_schema_from_transport=True)

    # Another way
    transport = RequestsHTTPTransport(url=url, use_json=True, auth=HTTPBasicAuth("fake", "situation"))
    try:
        Client(retries=3, transport=transport, fetch_schema_from_transport=True)
    except Exception as e:
        assert type(e) == requests.exceptions.HTTPError
        assert e.response.status_code == 401

    password = "MyHonestSaltPassword"
    some_user.set_password(password)
    some_user.save()
    transport = RequestsHTTPTransport(url=url, use_json=True, auth=HTTPBasicAuth(some_user.username, password))
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

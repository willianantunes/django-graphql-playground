import uuid

import pytest
from graphene.test import Client

from django_graphql_playground.apps.core.models import Category
from django_graphql_playground.apps.core.models import Ingredient
from django_graphql_playground.apps.gqyl.schema import schema


@pytest.fixture
def client():
    return Client(schema)


@pytest.fixture
def prepare_db():
    fake_category_name = "fake-category-name"
    fake_category = Category.objects.create(name=fake_category_name)
    fake_ingredient_notes = "fake_ingredient_notes"
    fake_ingredient_name = "fake_ingredient_name"
    fake_ingredient = Ingredient.objects.create(
        name=fake_ingredient_name, notes=fake_ingredient_notes, category=fake_category
    )
    yield fake_category, fake_ingredient


@pytest.mark.django_db
def test_should_retrieve_all_categories(client, prepare_db):
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
    executed = client.execute(query)

    assert len(executed["data"]["allCategories"]) == 1
    created_category = executed["data"]["allCategories"][0]
    assert created_category["id"] is not None
    assert created_category["name"] == "fake-category-name"
    assert len(created_category["ingredients"]) == 1
    created_ingredient = created_category["ingredients"][0]
    assert created_ingredient["id"] is not None
    assert created_ingredient["name"] == "fake_ingredient_name"
    assert created_ingredient["notes"] == "fake_ingredient_notes"


@pytest.mark.django_db
def test_should_retrieve_specific_category(client, prepare_db):
    fake_category, _ = prepare_db

    def do_assert(category: dict) -> None:
        assert category["id"] == str(fake_category.id)
        assert category["name"] == fake_category.name

    query = f"""
        query {{
          category(id: "{str(fake_category.id)}"){{
            id
            name
            ingredients {{
              id
              name
              notes
            }}
          }}
        }}
    """
    executed = client.execute(query)
    do_assert(executed["data"]["category"])
    query = f"""
        query {{
          category(name: "{fake_category.name}"){{
            id
            name
            ingredients {{
              id
              name
              notes
            }}
          }}
        }}
    """
    executed = client.execute(query)
    do_assert(executed["data"]["category"])
    query = f"""
        query {{
          category(id: "{str(fake_category.id)}", name: "{fake_category.name}"){{
            id
            name
            ingredients {{
              id
              name
              notes
            }}
          }}
        }}
    """
    executed = client.execute(query)
    do_assert(executed["data"]["category"])


@pytest.mark.django_db
def test_should_retrieve_nothing_from_category(client, prepare_db):
    fake_category_id = uuid.uuid4()

    query = f"""
        query {{
          category(id: "{str(fake_category_id)}"){{
            id
            name
            ingredients {{
              id
              name
              notes
            }}
          }}
        }}
    """
    executed = client.execute(query)

    assert executed["data"]["category"] is None


@pytest.mark.django_db
def test_should_retrieve_categories_created_between_from_specific_date(client):
    Category.objects.create(name="fake-category-name-1", start_at="2019-03-01", end_at="2019-03-15")
    Category.objects.create(name="fake-category-name-2", start_at="2019-03-15", end_at="2019-03-31")

    query = """
        query {
          allCategoriesConfiguredBetweenTheDate(date: "2019-02-28") {
            id
          }
        }    
    """
    assert len(client.execute(query)["data"]["allCategoriesConfiguredBetweenTheDate"]) == 0

    query = """
        query {
          allCategoriesConfiguredBetweenTheDate(date: "2019-03-14") {
            id
          }
        }    
    """
    assert len(client.execute(query)["data"]["allCategoriesConfiguredBetweenTheDate"]) == 1

    query = """
        query {
          allCategoriesConfiguredBetweenTheDate(date: "2019-03-15") {
            id
          }
        }    
    """
    assert len(client.execute(query)["data"]["allCategoriesConfiguredBetweenTheDate"]) == 2

    query = """
        query {
          allCategoriesConfiguredBetweenTheDate(date: "2019-03-31") {
            id
          }
        }    
    """
    assert len(client.execute(query)["data"]["allCategoriesConfiguredBetweenTheDate"]) == 1

    query = """
        query {
          allCategoriesConfiguredBetweenTheDate(date: "2019-04-01") {
            id
          }
        }    
    """
    assert len(client.execute(query)["data"]["allCategoriesConfiguredBetweenTheDate"]) == 0


@pytest.mark.django_db
def test_should_retrieve_all_ingredients(client, prepare_db):
    query = """
        query {
          allIngredients{
            id
            name
            notes
            category {
              id
              name
            }
          }
        }
    """
    executed = client.execute(query)

    assert len(executed["data"]["allIngredients"]) == 1
    created_ingredient = executed["data"]["allIngredients"][0]
    assert created_ingredient["id"] is not None
    assert created_ingredient["name"] == "fake_ingredient_name"
    assert created_ingredient["notes"] == "fake_ingredient_notes"
    created_category = created_ingredient["category"]
    assert created_category["id"] is not None
    assert created_category["name"] == "fake-category-name"

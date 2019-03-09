import pytest
from graphene.test import Client

from api.graphql.schema import schema
from api.models import Category
from api.models import Ingredient


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
    assert created_category["id"] == "1"
    assert created_category["name"] == "fake-category-name"
    assert len(created_category["ingredients"]) == 1
    created_ingredient = created_category["ingredients"][0]
    assert created_ingredient["id"] == "1"
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
          category(id: {fake_category.id}){{
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
          category(id: {fake_category.id}, name: "{fake_category.name}"){{
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
    assert created_ingredient["id"] == "1"
    assert created_ingredient["name"] == "fake_ingredient_name"
    assert created_ingredient["notes"] == "fake_ingredient_notes"
    created_category = created_ingredient["category"]
    assert created_category["id"] == "1"
    assert created_category["name"] == "fake-category-name"

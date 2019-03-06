import pytest
from graphene.test import Client

from api.graphql.schema import schema
from api.models import Category, Ingredient


@pytest.fixture
def client():
    return Client(schema)


@pytest.fixture
def prepare_db():
    fake_category_name = "fake-category-name"
    fake_category = Category.objects.create(name=fake_category_name)
    fake_ingredient_notes = "fake_ingredient_notes"
    fake_ingredient_name = "fake_ingredient_name"
    Ingredient.objects.create(name=fake_ingredient_name, notes=fake_ingredient_notes, category=fake_category)


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


@pytest.mark.django_db
def test_should_create_category(client):
    query = """
        mutation createCategory($data: CategorySerializerMutationInput!){
            createCategory(input: $data){
            id
            name
            errors{
              messages
              field
            }
          }
        }     
    """
    query_variables = {"data": {"name": "fake-category"}}
    executed = client.execute(query, variable_values=query_variables)

    assert executed == {"data": {"createCategory": {"id": 1, "name": "fake-category", "errors": None}}}


@pytest.mark.django_db
def test_should_create_ingredient(client):
    fake_category_name = "fake_name_category"
    fake_category = Category.objects.create(name=fake_category_name)

    query = """
        mutation createIngredient($data: IngredientSerializerMutationInput!){
           createIngredient(input: $data) {
            id
            name
            notes
            category
            errors {
              field
              messages
            }
          }
        }
    """
    query_variables = {
        "data": {"name": "fake_ingredient_name", "notes": "fake_ingredient_notes", "category": fake_category.id}
    }
    executed = client.execute(query, variable_values=query_variables)

    assert executed == {
        "data": {
            "createIngredient": {
                "id": 1,
                "name": "fake_ingredient_name",
                "notes": "fake_ingredient_notes",
                "category": "1",
                "errors": None,
            }
        }
    }

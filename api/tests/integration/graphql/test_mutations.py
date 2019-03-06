import pytest
from graphene.test import Client

from api.graphql.schema import schema
from api.models import Category


@pytest.mark.django_db
def test_should_create_category():
    client = Client(schema)

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
def test_should_create_ingredient():
    client = Client(schema)

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

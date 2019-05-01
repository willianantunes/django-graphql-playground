import time
from datetime import datetime

import pytest
from graphene.test import Client

from django_graphql_playground.apps.core.models import Category
from django_graphql_playground.apps.gqyl.schema import schema


@pytest.fixture
def client():
    return Client(schema)


@pytest.mark.django_db
def test_should_create_category(client):
    query = """
        mutation createOrUpdateCategory($data: CategorySerializerMutationInput!){
            createOrUpdateCategory(input: $data){
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

    assert executed == {"data": {"createOrUpdateCategory": {"id": 1, "name": "fake-category", "errors": None}}}


@pytest.mark.django_db
def test_should_update_category(client):
    pattern = "%Y-%m-%d %H:%M %S"
    fake_category_name = "fake-name-1"
    fake_category = Category.objects.create(name=fake_category_name)
    assert fake_category.created_at.strftime(pattern) == fake_category.updated_at.strftime(pattern)

    query = """
        mutation createOrUpdateCategory($data: CategorySerializerMutationInput!){
            createOrUpdateCategory(input: $data){
            id
            name
            errors{
              messages
              field
            }
          }
        }     
    """
    query_variables = {"data": {"id": fake_category.id, "name": "fake-name-2"}}
    time.sleep(1)
    executed = client.execute(query, variable_values=query_variables)

    assert len(Category.objects.all()) == 1
    updated_fake_category = Category.objects.all().first()
    assert updated_fake_category.created_at.strftime(pattern) != updated_fake_category.updated_at.strftime(pattern)
    assert executed == {
        "data": {"createOrUpdateCategory": {"id": fake_category.id, "name": "fake-name-2", "errors": None}}
    }


@pytest.mark.django_db
def test_should_delete_category(client):
    fake_category_name = "fake-category-name"
    Category.objects.create(name=fake_category_name)
    query = """
        mutation deleteCategory {
          deleteCategory(name: "fake-category-name"){
            ok
          }
        }    
    """
    executed = client.execute(query)

    assert executed["data"]["deleteCategory"]["ok"] == True
    assert len(Category.objects.all()) == 0


@pytest.mark.django_db
def test_should_create_ingredient(client):
    fake_category_name = "fake_name_category"
    fake_category = Category.objects.create(name=fake_category_name)

    query = """
        mutation createOrUpdateIngredient($data: IngredientSerializerMutationInput!){
           createOrUpdateIngredient(input: $data) {
            id
            name
            notes
            category
            createdAt
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

    created_ingredient = executed["data"]["createOrUpdateIngredient"]
    assert created_ingredient["id"] == 1
    assert created_ingredient["name"] == "fake_ingredient_name"
    assert created_ingredient["notes"] == "fake_ingredient_notes"
    assert created_ingredient["category"] == "1"
    assert type(datetime.fromisoformat(created_ingredient["createdAt"])) is datetime
    assert created_ingredient["errors"] is None

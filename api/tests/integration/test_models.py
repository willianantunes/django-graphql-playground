import pytest
from django.db import IntegrityError

from api.models import Category
from api.models import Ingredient


@pytest.mark.django_db
def test_should_create_category():
    fake_category_name = "fake_name_category"
    Category.objects.create(name=fake_category_name)

    assert Category.objects.all().count() == 1
    assert Category.objects.all().first().name == fake_category_name


@pytest.mark.django_db
def test_should_create_an_ingredient_with_its_category():
    fake_category_name = "fake_name_category"
    fake_category = Category.objects.create(name=fake_category_name)

    fake_ingredient_notes = "fake_ingredient_notes"
    fake_ingredient_name = "fake_ingredient_name"
    Ingredient.objects.create(name=fake_ingredient_name, notes=fake_ingredient_notes, category=fake_category)

    fake_ingredient = Ingredient.objects.all().first()
    assert fake_ingredient.name == fake_ingredient_name
    assert fake_ingredient.notes == fake_ingredient_notes
    assert fake_ingredient.category == fake_category


@pytest.mark.django_db
def test_should_throw_constraint_error_when_category_id_is_invalid():
    fake_ingredient_notes = "fake_ingredient_notes"
    fake_ingredient_name = "fake_ingredient_name"

    with pytest.raises(IntegrityError) as exception:
        Ingredient.objects.create(name=fake_ingredient_name, notes=fake_ingredient_notes)

    assert str(exception.value) == "NOT NULL constraint failed: api_ingredient.category_id"

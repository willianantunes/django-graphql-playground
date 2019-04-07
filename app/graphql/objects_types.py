from graphene_django.types import DjangoObjectType

from app.models import Category
from app.models import Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient

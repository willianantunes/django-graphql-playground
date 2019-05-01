from graphene_django.types import DjangoObjectType

from django_graphql_playground.apps.core.models import Category
from django_graphql_playground.apps.core.models import Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient

import graphene

from api.graphql.objects_types import CategoryType, IngredientType
from api.models import Category, Ingredient


class QueryDefinition(object):
    all_categories = graphene.List(CategoryType)
    all_ingredients = graphene.List(IngredientType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_ingredients(self, info, **kwargs):
        return Ingredient.objects.all()

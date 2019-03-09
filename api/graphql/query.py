import graphene

from api.graphql.objects_types import CategoryType
from api.graphql.objects_types import IngredientType
from api.models import Category
from api.models import Ingredient


class QueryDefinition(object):
    all_categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, id=graphene.Int(), name=graphene.String())
    all_ingredients = graphene.List(IngredientType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_category(self, info, **kwargs):
        id = kwargs.get("id")
        name = kwargs.get("name")

        if id and name:
            return Category.objects.get(pk=id, name=name)
        if id:
            return Category.objects.get(pk=id)
        if name:
            return Category.objects.get(name=name)
        return None

    def resolve_all_ingredients(self, info, **kwargs):
        return Ingredient.objects.all()

import graphene

from api.graphql.objects_types import CategoryType
from api.graphql.objects_types import IngredientType
from api.models import Category
from api.models import Ingredient


class QueryDefinition(object):
    all_categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, id=graphene.Int(), name=graphene.String())
    all_categories_configured_between_the_date = graphene.List(CategoryType, date=graphene.Date(required=True))
    all_ingredients = graphene.List(IngredientType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_category(self, info, **kwargs):
        id = kwargs.get("id")
        name = kwargs.get("name")

        if id and name:
            return Category.objects.filter(id=id, name=name).first()
        if id:
            return Category.objects.filter(id=id).first()
        if name:
            return Category.objects.filter(name=name).first()
        return None

    def resolve_all_categories_configured_between_the_date(self, info, **kwargs):
        date = kwargs["date"]
        return Category.objects.filter(start_at__lte=date, end_at__gte=date)

    def resolve_all_ingredients(self, info, **kwargs):
        return Ingredient.objects.all()

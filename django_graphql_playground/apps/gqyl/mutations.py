import graphene
from graphene_django.rest_framework.mutation import SerializerMutation

from django_graphql_playground.apps.core.models import Category
from django_graphql_playground.apps.drf.serializers import CategorySerializer
from django_graphql_playground.apps.drf.serializers import IngredientSerializer


class CategorySerializerMutation(SerializerMutation):
    class Meta:
        serializer_class = CategorySerializer


class DeleteCategory(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info, name):
        ok = False
        category = Category.objects.filter(name=name)
        if category:
            category.delete()
            ok = True
        return DeleteCategory(ok=ok)


class IngredientSerializerMutation(SerializerMutation):
    class Meta:
        serializer_class = IngredientSerializer


class Mutations(graphene.ObjectType):
    create_or_update_category = CategorySerializerMutation.Field()
    delete_category = DeleteCategory.Field()
    create_or_update_ingredient = IngredientSerializerMutation.Field()

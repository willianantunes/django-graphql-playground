import graphene
from graphene_django.rest_framework.mutation import SerializerMutation

from api.drf.serializers import CategorySerializer
from api.drf.serializers import IngredientSerializer
from api.models import Category


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
    create_category = CategorySerializerMutation.Field()
    delete_category = DeleteCategory.Field()
    create_ingredient = IngredientSerializerMutation.Field()

import graphene
from graphene_django.rest_framework.mutation import SerializerMutation

from api.drf.serializers import CategorySerializer, IngredientSerializer


class CategorySerializerMutation(SerializerMutation):
    class Meta:
        serializer_class = CategorySerializer


class IngredientSerializerMutation(SerializerMutation):
    class Meta:
        serializer_class = IngredientSerializer


class Mutations(graphene.ObjectType):
    create_category = CategorySerializerMutation.Field()
    create_ingredient = IngredientSerializerMutation.Field()

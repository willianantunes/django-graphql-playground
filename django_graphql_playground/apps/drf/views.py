from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django_graphql_playground.apps.core.models import Category
from django_graphql_playground.apps.core.models import Ingredient
from django_graphql_playground.apps.drf.serializers import CategorySerializer
from django_graphql_playground.apps.drf.serializers import IngredientSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticated,)

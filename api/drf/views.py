from rest_framework import viewsets

from api.drf.serializers import CategorySerializer, IngredientSerializer
from api.models import Category, Ingredient


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.drf.serializers import CategorySerializer
from api.drf.serializers import IngredientSerializer
from api.models import Category
from api.models import Ingredient


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticated,)

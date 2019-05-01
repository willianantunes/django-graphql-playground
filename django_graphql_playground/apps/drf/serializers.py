from rest_framework import serializers

from django_graphql_playground.apps.core.models import Category
from django_graphql_playground.apps.core.models import Ingredient


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "created_at", "updated_at", "start_at", "end_at")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category", "created_at", "updated_at")

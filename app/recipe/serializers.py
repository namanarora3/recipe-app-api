from rest_framework.serializers import ModelSerializer
from core.models import Recipe

class RecipeSerializer(ModelSerializer):
    '''Serializer for Recipe'''
    class  Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'description', 'link', 'price']
        read_only_fields = ['id']

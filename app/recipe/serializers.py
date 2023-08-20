from rest_framework.serializers import ModelSerializer
from core.models import Recipe, Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(ModelSerializer):

    tags = TagSerializer(many=True, required=False)

    '''Serializer for Recipe'''

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes',
                  'description', 'link', 'price', 'tags']
        read_only_fields = ['id']

    def _get_or_create_tags(self, recipe, tags):
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(recipe, tags)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(instance, tags)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class RecipeDetailSerialiser(RecipeSerializer):
    class meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']

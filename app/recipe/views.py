'''Views for the Recipe APIs'''

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import (
    Recipe,
    Tag,
    Ingredient
)
from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
    TagSerializer,
    IngredientSerializer,
    RecipeImageSerializer
)


class RecipeViewSet(viewsets.ModelViewSet):
    '''View for manage recipe APIs'''
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # overwrite get_queryset() method
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        print(self.action)
        if self.action == "partial_update":
            return RecipeDetailSerializer
        if self.action == 'list':
            return RecipeSerializer
        elif self.action == 'upload_image':
            return RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        '''Create a new recipe'''
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BaseRecipeAttrViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    '''Base viewSet for recipe attributes'''
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BaseRecipeAttrViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

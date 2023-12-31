'''
URLs for the Recipe app
'''

from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
    path('public/', views.PublicRecipeView.as_view({'get': 'list'}), name='public'),
    path('public/<int:pk>/', views.PublicRecipeDetailView.as_view())

]

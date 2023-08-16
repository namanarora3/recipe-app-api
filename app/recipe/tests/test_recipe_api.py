'''tests for recipe APIs'''

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status
# from rest_framework
from core.models import Recipe

from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')

def create_recipe(user,**params):
  '''create a recipe using given contitions'''
  defaults = {
    'title': 'Sample title',
    'description': 'Sample description',
    'price': Decimal('22.5'),
    'time_minutes': 24,
    'link': 'http://example.com/recipe.pdf'
  }
  defaults.update(params)

  return Recipe.objects.create(user=user,**defaults)


class PublicRecipeAPITests(TestCase):
  '''test unauthenticated api requests'''
  def setUp(self) -> None:
    self.client = APIClient

  def test_auth_required(self):
    '''Test for auth is reqd to call API.'''
    res = self.client.get(RECIPES_URL)

    self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeAPITest(TestCase):
  '''test authenticated api requests'''

  def setUp(self) -> None:
    self.client = APIClient
    self.user = get_user_model().objects.create(
      email='test@example.com',
      password='testpass123',
      name='Test User'
    )
    self.client.force_authenticate(self.user)

  def test_retrive_recipes(self):
    '''Test receiving a list of recipes'''
    create_recipe(user=self.user, title='r1')
    create_recipe(user=self.user, title='r2')

    res = self.client.get(RECIPES_URL)

    recipes = Recipe.objects.all().order_by('-id')
    serialized = RecipeSerializer(recipes,many=True)

    self.assertEqual(res.status_code,status.HTTP_200_OK)
    self.assertEqual(res.data,serialized.data)

  def test_recipe_list_limited_to_user(self):
    user2 = get_user_model().objects.create(
      'test2@example.com',
      'test123'
    )
    create_recipe(user=user2)
    create_recipe(user=self.user)

    res = self.client.get(RECIPES_URL)

    recipes = Recipe.objects.filter(user=self.user).order_by('-id')
    serialized = RecipeSerializer(recipes,many=True)

    self.assertEqual(res.status_code,status.HTTP_200_OK)
    self.assertEqual(res.data,serialized.data)





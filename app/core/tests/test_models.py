'''
tests for models
'''

from django.test import TestCase
# helper func to get def django user model for proj
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models


def create_user():
    user = get_user_model().objects.create_user(
        "test@example.com",
        "testpass123"
    )
    return user


class ModelTests(TestCase):
    """ adding all tests for user model here"""

    def test_create_user_with_email_successful(self):
        """ test for creating users"""
        email = 'test@example.com'
        password = 'testpass123'
        # create_user is a custom method
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        # check_password is provided by baseUserManager
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        ''' test email is normalised'''

        sample_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_email:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        ''' creating user without email address raises ValueError'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test@123')

    def test_create_superuser(self):
        '''test creating a super user'''
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        '''Test creating recipe is successful'''
        user = create_user()
        recipe = models.Recipe.objects.create(
            user=user,
            title='sample recipe name',
            time_minutes=5,
            price=Decimal(5.50),
            description='Sample recipe description'
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        '''teat creating a tag is successful'''
        user = create_user()
        tag = models.Tag.objects.create(
            user=user,
            name="sample tag"
        )
        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingredient is successful."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient1'
        )

        self.assertEqual(str(ingredient), ingredient.name)

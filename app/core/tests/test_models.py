# '''
# tests for models
# '''

# from django.test import TestCase
# #helper func to get def django user model for proj
# from django.contrib.auth import get_user_model

# class ModelTests(TestCase):
#     """ adding all tests for user model here"""

#     def test_create_user_with_email_successful(self):
#         """ test for creating users"""
#         email = "test@example.com"
#         password = "testpass@123"
#         #create_user is a custom method
#         user = get_user_model().objects.create_user(
#             email = email,
#             password = password
# 		)
#         self.assertEqual(user.email, email)
#         #check_password is provided by baseUserManager
#         self.assertTrue(user.check_password(password))
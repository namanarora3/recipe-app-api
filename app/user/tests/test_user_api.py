'''
tests for User API
'''


from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
CREATE_TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    '''create and return a new user'''
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'email':'te5465st@example.com',
            'password':'testpass',
            'name':'Test User'
        }

        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email = payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)

    def test_duplicate_email_error(self):
        '''test error returned if user with same email already exists'''
        payload = {
            'email':'test@example.com',
            'password':'testpass@1234',
            # 'name':'Test User'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        '''returns error if password < 5 chars'''
        payload = {
            'email':'test@example.com',
            'password':'tes',
            # 'name':'Test User'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token(self):
        '''test for testing token creation'''
        payload = {
            'email':'test@example.com',
            'password':'tes',
            'name':'Test User'
        }

        create_user(**payload)
        res = self.client.post(CREATE_TOKEN_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertIn('token',res.data)

    def test_bad_credentials(self):
        '''test for checking system response for wrong credentials'''
        payload = {
            'email':'test@example.com',
            'password':'tes',
            'name':'Test User'
        }
        create_user(**payload)
        payload['password'] = 'changed'
        res = self.client.post(CREATE_TOKEN_URL,payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_blank_pass_credentials(self):
        '''test for checking system response for blank'''
        payload = {
            'email':'test@example.com',
            'password':'tes',
            'name':''
        }
        res = self.client.post(CREATE_TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_unauthorised(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateUserAPITests(TestCase):
    '''Test API requests that require authentication'''
    def setUp(self):
        user_details = {
            'name':'Test User',
            'email':'test@example.com',
            'password':'testpass123'
        }
        self.user = create_user(**user_details)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrive_profile_success(self):
        '''test retriving profile for logged in user'''
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,{
            'name':self.user.name,
            'email':self.user.email
        })

    def test_post_not_allowed(self):

        res = self.client.post(ME_URL,{})
        '''TEST post method isnt allowed for me endpoint'''
        self.assertEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_profile_updated(self):
        '''test for updating me data'''
        payload = {
            'name':'updatedname',
            'password':'newpass123'
        }

        res = self.client.patch(ME_URL,payload)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(payload['name'],self.user.name)
        self.assertTrue(self.user.check_password(payload['password']))











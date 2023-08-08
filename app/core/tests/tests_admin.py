''' unit tests for django admin modification'''

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
# from ..models import User


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin2@example.com",
            password="naman"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user2@example.com",
            password="naman",
            name="test_user"
        )

    def test_users_list(self):
        ''' Method that tests if user table exists'''
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user(self):
        '''test to check add user is working or not'''
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_add_user(self):
        '''test to create user page works'''
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

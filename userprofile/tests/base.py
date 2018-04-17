from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import resolve
from rest_framework.test import APIRequestFactory, force_authenticate


class UserProfileBaseTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = APIRequestFactory()
        self.user_details = {
            'email': "otheruser@mail.com",
            'name': "Other User",
            'password': "Password01",
        }
        self.user = get_user_model().objects.create_user(
            self.user_details['email'],
            password=self.user_details['password'],
            name=self.user_details['name']
        )
        self.user.profile.address = '123 Fake St'
        self.user.profile.save()
        self.admin_user_details = {
            'email': "admin@mail.com",
            'name': 'Admin User',
            'password': 'Password01'
        }
        self.admin_user = get_user_model().objects.create_superuser(
            email=self.admin_user_details['email'],
            password=self.admin_user_details['password'],
            name=self.admin_user_details['name']
        )

    def get_request(self, url, action='get', data=None, user=None):
        if data:
            request = getattr(self.factory, action)(url, data, format='json')
        else:
            request = getattr(self.factory, action)(url, format='json')
        if user:
            force_authenticate(request, user)
        return request

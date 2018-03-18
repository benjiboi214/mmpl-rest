import re

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail
from rest_framework.test import APIClient


class FunctionalRestTest(StaticLiveServerTestCase):
    def setUp(self):
        self.client = APIClient()
        # Regular user for API access
        self.other_user = {
            'email': "otheruser@mail.com",
            'name': "Other User",
            'password': "Password01",
        }
        get_user_model().objects.create_user(
            self.other_user['email'],
            password=self.other_user['password'],
            name=self.other_user['name'])
        # Admin user for privileged operations
        self.admin_user = {
            'email': "admin@mail.com",
            'name': "Admin User",
            'password': "Password01",
        }
        get_user_model().objects.create_superuser(
            email=self.admin_user['email'],
            password=self.admin_user['password'],
            name=self.admin_user['name']
        )

    def create_jwt(self, email, password):
        return self.client.post(
            '/auth/jwt/create/',
            {
                'email': email,
                'password': password
            },
            format='json'
        )

    def get_uid_and_token_from_email(self, regex, email_index):
        email = mail.outbox[email_index]
        search = re.search(regex, email.body)
        uid = search.group(1)
        token = search.group(2)
        return (uid, token)

    def check_me_endpoint(self, user_name, user_jwt):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + user_jwt)
        response = self.client.get(
            '/auth/me/',
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(user_name, response.data['name'])

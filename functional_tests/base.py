import re

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail
from rest_framework.test import APIClient


class FunctionalRestTest(StaticLiveServerTestCase):
    def setUp(self):
        self.created_profiles = 0
        self.client = APIClient()

    def create_staff_user(self):
        self.staff_user_details = {
            'email': "staff@mail.com",
            'name': "Staff User",
            'password': "Password01",
        }
        self.staff_user = get_user_model().objects.create_user(
            self.staff_user_details['email'],
            password=self.staff_user_details['password'],
            name=self.staff_user_details['name']
        )
        self.staff_user.is_staff = True
        self.staff_user.save()
        self.created_profiles += 1
        return self.staff_user_details

    def create_user(self):
        self.user_details = {
            'email': 'user@mail.com',
            'name': 'Regular User',
            'password': 'Password01'
        }
        self.user = get_user_model().objects.create_user(
            self.user_details['email'],
            password=self.user_details['password'],
            name=self.user_details['name']
        )
        self.user.save()
        self.created_profiles += 1
        return self.user_details

    def create_other_user(self):
        self.other_user_details = {
            'email': 'other_user@mail.com',
            'name': 'Other Regular User',
            'password': 'Password01'
        }
        self.other_user = get_user_model().objects.create_user(
            self.other_user_details['email'],
            password=self.other_user_details['password'],
            name=self.other_user_details['name']
        )
        self.other_user.save()
        self.created_profiles += 1
        return self.other_user_details

    def authenticate(self, user_details=None):
        if user_details:
            token = self.create_jwt(
                user_details['email'],
                user_details['password']
            ).data['token']
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
            return token
        else:
            self.client.credentials()
            return None

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

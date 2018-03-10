from django.contrib.auth import get_user_model
from django.test import TestCase


class UserProfileBaseTest(TestCase):
    def setUp(self):
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

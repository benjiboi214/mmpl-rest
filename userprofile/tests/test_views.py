from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import permissions
from rest_framework.test import force_authenticate, APIRequestFactory

from userprofile.views import MyProfileDetail


class TestPlayerView(TestCase):
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
        self.factory = APIRequestFactory()
        self.view = MyProfileDetail.as_view()

    def test_view_available_to_authenticated_user(self):
        # testing the authentication class is present
        request = self.factory.get('/profiles/me')
        force_authenticate(request, self.user)
        response = self.view(request)
        self.assertEqual(200, response.status_code)

    def test_view_not_available_to_unauthenticated_user(self):
        request = self.factory.get('/profiles/me')
        response = self.view(request)
        self.assertEqual(401, response.status_code)
    
    def test_get_profile_method_success(self):
        # test helper method for getting the profile based on the user rtequest when it should succeed.
        user_profile = MyProfileDetail.get_player_object(self, self.user)
        self.assertEqual(self.user.profile, user_profile)
    
    def test_get_profile_method_failure(self):
        # test helper method for getting the profile based on the user request when it should fail.
        user = get_user_model().objects.create()
        user_profile = MyProfileDetail.get_player_object(self, user)
        self.assertEqual(user.profile, user_profile)

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import permissions

from userprofile.views import ProfileMe, ProfileList
from utils import permissions as custom_permissions
from .base import UserProfileBaseTest


class TestProfileMeView(UserProfileBaseTest):

    def test_view_available_to_authenticated_user(self):
        response = self.get_view_response(
            'get',
            reverse('profile-me'),
            user=self.user)
        self.assertEqual(200, response.status_code)

    def test_view_not_available_to_unauthenticated_user(self):
        response = self.get_view_response(
            'get',
            reverse('profile-me'))
        self.assertEqual(401, response.status_code)

    def test_get_profile_method_success(self):
        user_profile = ProfileMe.get_player_object(self, self.user)
        self.assertEqual(self.user.profile, user_profile)

    def test_get_profile_method_failure(self):
        user = get_user_model().objects.create()
        user_profile = ProfileMe.get_player_object(self, user)
        self.assertEqual(user.profile, user_profile)

    def test_get_returns_correct_profile(self):
        response = self.get_view_response(
            'get',
            reverse('profile-me'),
            user=self.user)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.user.profile.address, response.data['address'])

    def test_put_updates_profile(self):
        new_address = '321 Ekaf Ts'
        response = self.get_view_response(
            'put',
            reverse('profile-me'),
            data={'address': new_address},
            user=self.user)
        self.assertEqual(new_address, response.data['address'])

    def test_put_invalid_data_throws_error(self):
        long_address = '''
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque
        tincidunt neque quis ullamcorper blandit. Pellentesque sit amet
        pharetra dolor. Sed in posuere velit. Curabitur eu auctor magna.
        Blah Blah.o
        '''
        response = self.get_view_response(
            'put',
            reverse('profile-me'),
            data={'address': long_address},
            user=self.user)
        self.assertEqual(400, response.status_code)
        self.assertIn(
            'no more than 200 characters.', response.data['address'][0])


class TestProfileListView(UserProfileBaseTest):

    def test_viewset_list_shows_list_of_profiles(self):
        response = self.get_view_response(
            'get',
            reverse('profile-list'),
        )
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.data)
        self.assertEqual(1, len(response.data))

    def test_viewset_get_queryset_action_list(self):
        view = ProfileList()
        view.action = 'list'
        view_permissions = view.get_permissions()
        self.assertIsInstance(
            view_permissions[0],
            custom_permissions.IsAdminOrReadOnly
        )

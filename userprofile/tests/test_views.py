from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.test import APIRequestFactory, force_authenticate

from userprofile.views import MyProfileDetail

from .base import UserProfileBaseTest


class TestPlayerView(UserProfileBaseTest):

    def get_view_response(self, action, data=None, authenticate=False):
        factory = APIRequestFactory()
        view = MyProfileDetail.as_view()
        if data:
            request = getattr(factory, action)(
                '/profiles/me', data, format='json')
        else:
            request = getattr(factory, action)(
                '/profiles/me')
        if authenticate:
            force_authenticate(request, self.user)
        return view(request)

    def test_view_available_to_authenticated_user(self):
        response = self.get_view_response('get', authenticate=True)
        self.assertEqual(200, response.status_code)

    def test_view_not_available_to_unauthenticated_user(self):
        response = self.get_view_response('get')
        self.assertEqual(401, response.status_code)

    def test_get_profile_method_success(self):
        user_profile = MyProfileDetail.get_player_object(self, self.user)
        self.assertEqual(self.user.profile, user_profile)

    def test_get_profile_method_failure(self):
        user = get_user_model().objects.create()
        user_profile = MyProfileDetail.get_player_object(self, user)
        self.assertEqual(user.profile, user_profile)

    def test_get_returns_correct_profile(self):
        response = self.get_view_response('get', authenticate=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.user.profile.address, response.data['address'])

    def test_put_updates_profile(self):
        new_address = '321 Ekaf Ts'
        response = self.get_view_response(
            'put', data={'address': new_address}, authenticate=True)
        self.assertEqual(new_address, response.data['address'])

    def test_put_invalid_data_throws_error(self):
        long_address = '''
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque
        tincidunt neque quis ullamcorper blandit. Pellentesque sit amet
        pharetra dolor. Sed in posuere velit. Curabitur eu auctor magna.
        Blah Blah.o
        '''
        response = self.get_view_response(
            'put', data={'address': long_address}, authenticate=True)
        self.assertEqual(400, response.status_code)
        self.assertIn(
            'no more than 200 characters.', response.data['address'][0])

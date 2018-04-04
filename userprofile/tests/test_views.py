from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import permissions

from userprofile.views import ProfileMe, ProfileList, ProfileDetail
from utils import permissions as custom_permissions
from .base import UserProfileBaseTest
from userprofile.models import Profile


class TestProfileMeView(UserProfileBaseTest):

    def test_get_profile_method_success(self):
        user_profile = ProfileMe.get_player_object(self, self.user)
        self.assertEqual(self.user.profile, user_profile)

    def test_get_profile_method_failure(self):
        user = get_user_model().objects.create()
        user_profile = ProfileMe.get_player_object(self, user)
        self.assertEqual(user.profile, user_profile)

    def test_view_available_to_authenticated_user(self):
        url = reverse('profile-me')
        request = self.get_request(url, user=self.user)
        response = ProfileMe.as_view()(request)
        self.assertEqual(200, response.status_code)

    def test_view_not_available_to_unauthenticated_user(self):
        url = reverse('profile-me')
        request = self.get_request(url)
        response = ProfileMe.as_view()(request)
        self.assertEqual(401, response.status_code)

    def test_get_returns_correct_profile(self):
        url = reverse('profile-me')
        request = self.get_request(url, user=self.user)
        response = ProfileMe.as_view()(request)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.user.profile.address, response.data['address'])

    def test_put_updates_profile(self):
        url = reverse('profile-me')
        update_data = {'address': '321 Ekaf Ts'}
        request = self.get_request(
            url,
            action='put',
            data=update_data,
            user=self.user)
        response = ProfileMe.as_view()(request)
        self.assertEqual(200, response.status_code)
        self.assertEqual(update_data['address'], response.data['address'])

    def test_put_invalid_data_throws_error(self):
        url = reverse('profile-me')
        update_data = {'address': '''
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque
        tincidunt neque quis ullamcorper blandit. Pellentesque sit amet
        pharetra dolor. Sed in posuere velit. Curabitur eu auctor magna.
        Blah Blah.o '''}
        request = self.get_request(
            url,
            action='put',
            data=update_data,
            user=self.user
        )
        response = ProfileMe.as_view()(request)
        self.assertEqual(400, response.status_code)
        self.assertIn(
            'no more than 200 characters.', response.data['address'][0])


class TestProfileListView(UserProfileBaseTest):

    def test_get_shows_list_of_profiles(self):
        url = reverse('profile-list')
        request = self.get_request(url)
        response = ProfileList.as_view()(request)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.data)
        self.assertEqual(2, len(response.data))

    def test_get_permissions_instance(self):
        view = ProfileList()
        view.action = 'get'
        view_permissions = view.get_permissions()
        self.assertIsInstance(
            view_permissions[0],
            custom_permissions.IsAdminOrReadOnly
        )


class TestProfileDetailView(UserProfileBaseTest):

    def test_get_permissions_instance(self):
        view = ProfileDetail()
        view.action = 'get'
        view_permissions = view.get_permissions()
        self.assertIsInstance(
            view_permissions[0],
            custom_permissions.IsAdminOrReadOnly
        )
        self.assertIsInstance(
            view_permissions[1],
            custom_permissions.IsAuthenticatedAndProfileOwnerOrReadOnly
        )

    def test_update_profile(self):
        url = reverse('profile-detail', args=[self.user.profile.uuid])
        update_data = {'name': 'New Name!'}
        request = self.get_request(
            url,
            action='put',
            data=update_data,
            user=self.admin_user)
        response = ProfileDetail.as_view()(
            request,
            uuid=self.user.profile.uuid)
        self.assertEqual(200, response.status_code)
        self.assertEqual(update_data['name'], response.data['name'])

    def test_delete_profile(self):
        url = reverse('profile-detail', args=[self.user.profile.uuid])
        request = self.get_request(
            url, action='delete',
            user=self.admin_user)
        response = ProfileDetail.as_view()(
            request,
            uuid=self.user.profile.uuid)
        self.assertEqual(204, response.status_code)

    def test_get_profile(self):
        url = reverse('profile-detail', args=[self.user.profile.uuid])
        request = self.get_request(url)
        response = ProfileDetail.as_view()(
            request,
            uuid=self.user.profile.uuid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.user.profile.uuid.__str__(),
            response.data['uuid'])

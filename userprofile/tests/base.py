from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve
from rest_framework.test import APIRequestFactory, force_authenticate


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

    def get_view_response(self, action, url, data=None, user=False, uuid=None):
        factory = APIRequestFactory()
        view = resolve(url).func
        if data:
            request = getattr(factory, action)(
                url, data, format='json')
        else:
            request = getattr(factory, action)(url)
        if user:
            force_authenticate(request, user)
        if uuid:
            return view(request, uuid=uuid)
        else:
            return view(request)

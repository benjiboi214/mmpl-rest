from django.contrib.auth import get_user_model
from django.test import TestCase

from userprofile.models import Profile
from utils.models import User


class UserModelTest(TestCase):

    def test_user_model_is_set_in_settings(self):
        settings_model = get_user_model()
        self.assertEqual(settings_model, User)

    def test_object_manager_creates_user_profile(self):
        User = get_user_model()
        new_user = User.objects.create_user('test@mail.com', 'Password01')
        self.assertIsInstance(new_user.profile, Profile)

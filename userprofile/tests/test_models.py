from django.test import TestCase

from userprofile.models import Profile

from .base import UserProfileBaseTest


class TestPlayerView(UserProfileBaseTest):

    def test_related_name_works_from_user(self):
        related_profile = self.user.profile
        get_profile = Profile.objects.get(user=self.user)
        self.assertEqual(get_profile, related_profile)

    def test_on_delete_sets_user_to_null(self):
        profile = Profile.objects.get(user=self.user)
        self.user.delete()
        profile.refresh_from_db()
        self.assertIsNone(profile.user)

    def test_string_representation(self):
        self.user.profile.name = self.user_details['name']
        self.user.profile.save()
        self.assertEqual(self.user_details['name'], str(self.user.profile))

    def test_verbose_name_plural(self):
        self.assertEqual(str(Profile._meta.verbose_name_plural), "profiles")

    def test_saving_model_generates_uuid(self):
        profile = Profile.objects.create()
        self.assertIsNotNone(profile.uuid)

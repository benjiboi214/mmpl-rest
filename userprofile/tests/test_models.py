from django.test import TestCase

from userprofile.models import Profile

from .base import UserProfileBaseTest


class TestPlayerView(UserProfileBaseTest):
    
    def test_related_name_works_from_user(self):
        related_profile = self.user.profile # related name
        get_profile = Profile.objects.get(user=self.user)
        self.assertEqual(get_profile, related_profile)

    def test_on_delete_sets_user_to_null(self):
        profile = Profile.objects.get(user=self.user)
        self.user.delete()
        profile.refresh_from_db()
        self.assertIsNone(profile.user)
    
    def test_can_set_address_field(self):
        profile = Profile.objects.create(address="123 Fake St")
        profile.save()
        self.assertEqual(profile.address, '123 Fake St')

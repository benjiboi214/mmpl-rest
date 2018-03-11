from django.test import TestCase
from userprofile.serializers import ProfileSerializer
from userprofile.models import Profile


class ProfileSerializerTest(TestCase):

    def test_model_set_to_user_profile(self):
        serializer = ProfileSerializer()
        self.assertEqual(Profile, serializer.Meta.model)

    def test_address_field_on_serializer(self):
        serializer = ProfileSerializer()
        self.assertIn('address', serializer.fields)

from utils.models import User
from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):
    
    # Write custom model manager

    # Write custom User Model

    def test_user_model_is_set_in_settings(self):
        settings_model = get_user_model()
        self.assertEqual(settings_model, User)

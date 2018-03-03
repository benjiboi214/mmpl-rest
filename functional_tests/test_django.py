import re
import time
from unittest import skip

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model

from django.core import mail
from django.test.utils import override_settings
from rest_framework.test import APIClient
from selenium import webdriver


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()
    
    @skip
    @override_settings(DEBUG=True)
    def test_django_installed(self):
        self.browser.get(self.live_server_url)
        time.sleep(4)
        self.assertIn('Django', self.browser.title)

class FunctionalRESTTest(StaticLiveServerTestCase):
    def setUp(self):
        self.client = APIClient()
        self.other_user = {
            'email': "otheruser@mail.com",
            'name': "Other User",
            'password': "Password01",
        }
        test_user = get_user_model().objects.create_user(self.other_user['email'], password=self.other_user['password'])
        test_user.name = self.other_user['name']
        test_user.save()
    
    def create_jwt(self, email, password):
        return self.client.post(
            '/auth/jwt/create/',
            {
                'email': email,
                'password': password
            },
            format='json'
        )
    
    def get_uid_and_token_from_email(self, regex, email_index):
        email = mail.outbox[email_index]
        search = re.search(regex, email.body)
        uid = search.group(1)
        token = search.group(2)
        return (uid, token)

    def check_me_endpoint(self, user_name, user_jwt):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + user_jwt)
        response = self.client.get(
            '/auth/me/',
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(user_name, response.data['name'])

    def test_user_can_register_and_login(self):
        user = {
            'email': 'testing@mail.com',
            'name': 'Tester01',
            'password': 'Password01',
            'jwt': None,
        }

        # User then tries to create user with an email and not a username
        response = self.client.post(
            '/auth/users/create/',
            {
                'email': user['email'],
                'name': user['name'],
                'password': user['password']
            },
            format='json'
        )
        self.assertEquals(201, response.status_code)
        self.assertIn(user['email'], response.data['email'])

        # User gets the registration email from their mailbox
        uid, token = self.get_uid_and_token_from_email('#\/activate\/(.*?)\/(.*?)\\n', 0)

        # User verifies the activation by posting to the activate endpoint
        response = self.client.post(
            '/auth/users/activate/',
            {
                'uid': uid,
                'token': token
            },
            format='json'
        )
        self.assertEquals(204, response.status_code)
        confirmation_email = mail.outbox[1]
        self.assertIn('Your account has been created', confirmation_email.body)

        # User users their newly activated account to create a JWT
        response = self.create_jwt(user['email'], user['password'])
        self.assertEquals(200, response.status_code)
        self.assertIn('token', response.data)
        user['jwt'] = response.data['token']
        
        # User can use the new JWT to make a series of authenticated requests, such as the user endpoint
        self.check_me_endpoint(user['name'], user['jwt'])
    
    def test_user_can_change_password(self):
        # Pre-existing user logs in by asking for a JWT
        response = self.create_jwt(self.other_user['email'], self.other_user['password'])
        self.assertEquals(200, response.status_code)
        self.assertIn('token', response.data)
        self.other_user['jwt'] = response.data['token']

        # User wants to change their password, so they call the password change endpoint.
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.other_user['jwt'])
        new_password = 'Password02'
        response = self.client.post(
            '/auth/password/',
            {
                "new_password": new_password,
                "re_new_password": new_password,
                "current_password": self.other_user['password']
            },
            format='json'
        )
        self.assertEquals(204, response.status_code)

        # Once complete, user ensures the old password no longer works
        self.client.credentials()
        response = self.create_jwt(self.other_user['email'], self.other_user['password'])
        self.assertEquals(400, response.status_code)
        self.assertNotIn('token', response.data)

        # User logs in with their new password.
        response = self.create_jwt(self.other_user['email'], new_password)
        self.assertEquals(200, response.status_code)
        self.assertIn('token', response.data)
        self.other_user['jwt'] = response.data['token']

        # User gets their profile information
        self.check_me_endpoint(self.other_user['name'], self.other_user['jwt'])
    
    def test_user_can_reset_password(self):
        # User want to reset their password as they have forgotten it.
        # User makes call to the forgotten password endpoint
        response = self.client.post(
            '/auth/password/reset/',
            {'email': self.other_user['email']}
        )
        self.assertEqual(204, response.status_code)

        # User retrieves the email from their inbox.
        uid, token = self.get_uid_and_token_from_email('#\/password\/reset\/confirm\/(.*?)\/(.*?)\\n', 0)

        # User makes call to the reset confirm endpoint with uid, token and new password
        new_password = 'Password02'
        response = self.client.post(
            '/auth/password/reset/confirm/',
            {
                "uid": uid,
                "token": token,
                "new_password": new_password
            },
            format='json'
        )
        self.assertEqual(204, response.status_code)

        # User cannot log in with old password
        response = self.create_jwt(self.other_user['email'], self.other_user['password'])
        self.assertEqual(400, response.status_code)
        self.assertNotIn('token', response.data)

        # User can now create a JWT with the new password
        response = self.create_jwt(self.other_user['email'], new_password)
        self.assertEqual(200, response.status_code)
        self.assertIn('token', response.data)
        self.other_user['jwt'] = response.data['token']

        # User can now see their details with the created JWT.
        self.check_me_endpoint(self.other_user['name'], self.other_user['jwt'])

    def test_user_can_change_email_address(self):
        # Existing User logs in by creating JWT
        response = self.create_jwt(self.other_user['email'], self.other_user['password'])
        self.assertEqual(200, response.status_code)
        self.assertIn('token', response.data)
        self.other_user['jwt'] = response.data['token']

        # User posts to the change email address endpoint
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.other_user['jwt'])
        new_email = 'test2@mail.com'
        response = self.client.post(
            '/auth/email/',
            {
                "current_password": self.other_user['password'],
                "new_email": new_email,
                "re_new_email": new_email
            },
            format='json'
        )
        self.assertEqual(204, response.status_code)

        # User gets the UID and Token from the activation email
        uid, token = self.get_uid_and_token_from_email('#\/activate\/(.*?)\/(.*?)\\n', 0)
        self.client.credentials()
        response = self.client.post(
            '/auth/users/activate/',
            {
                'uid': uid,
                'token': token
            },
            format='json'
        )
        self.assertEquals(204, response.status_code)
        confirmation_email = mail.outbox[1]
        self.assertIn('Your account has been created', confirmation_email.body)

        # User cannot log in with old email
        response = self.create_jwt(self.other_user['email'], self.other_user['password'])
        self.assertEqual(400, response.status_code)
        self.assertNotIn('token', response.data)

        # User can log in with new email address.
        response = self.create_jwt(new_email, self.other_user['password'])
        self.assertEqual(200, response.status_code)
        self.assertIn('token', response.data)
        self.other_user['jwt'] = response.data['token']
    
    @skip
    def test_can_delete_user(self):
        pass
        # Existing User logs in by creating new JWT.

        # User posts to delete endpoint, allowing them to remove their user credenetials

        # User's related details should not delete. No CASCADE!

        # User can not log in with existing details.
    
    @skip
    def test_can_refresh_and_verify_jwt(self):
        pass
        # Existing User logs in by creating new JWT.

        # User verify's the JWT that was created.

        # Change JWT payload by one char, verify should now not work.

        # User can then refresh originally generated JWT.

        # User can log in with newly refreshed JWT.

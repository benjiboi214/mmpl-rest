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
        ## TODO: Figure out why this is not login-able once set up.
        User = get_user_model()
        self.other_user = User()
        self.other_user.email = "otheruser@mail.com"
        self.other_user.name = "Other User"
        self.other_user.password = "Password01"
        self.other_user.is_active = True
        self.other_user.save()

    def test_user_can_register_and_login(self):
        client = APIClient()
        user = {
            'email': 'testing@mail.com',
            'name': 'Tester01',
            'password': 'Password01',
            'jwt': None,
        }

        # User then tries to create user with an email and not a username
        response = client.post(
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
        activation_email = mail.outbox[0]
        search = re.search('#\/activate\/(.*?)\/(.*?)\\n', activation_email.body)
        uid = search.group(1)
        token = search.group(2)

        # User verifies the activation by posting to the activate endpoint
        response = client.post(
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
        response = client.post(
            '/auth/jwt/create/',
            {
                'email': user['email'],
                'password': user['password']
            },
            format='json'
        )
        self.assertEquals(200, response.status_code)
        self.assertIn('token', response.data)
        user['jwt'] = response.data['token']
        
        # User can use the new JWT to make a series of authenticated requests, such as the user endpoint
        client.credentials(HTTP_AUTHORIZATION='JWT ' + user['jwt'])
        response = client.get(
            '/auth/me/',
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(user['name'], response.data['name'])
    
    @skip
    def test_user_can_reset_password(self):
        pass
        # Using the user created in setUp make request to password reset endpoint.
        # Intercept the password email
        # Make call to password change endpoint
        # login with new password.
    
    @skip
    def test_user_can_change_password(self):
        pass
        # Using the user created in setUp, login
        # make call to change password endpoint
        # logout
        # login with new password.

        # test if passing auth token to an is authenticated view will work or if more needs to be done.

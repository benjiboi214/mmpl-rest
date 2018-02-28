import time

from unittest import skip

from django.core import mail

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.utils import override_settings
from rest_framework.test import APIClient
from selenium import webdriver


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()
    
    @override_settings(DEBUG=True)
    def test_django_installed(self):
        self.browser.get(self.live_server_url)
        time.sleep(4)
        self.assertIn('Django', self.browser.title)

class FunctionalRESTTest(StaticLiveServerTestCase):

    def test_user_can_register_and_login(self):
        client = APIClient()

        # User tried to create a user with a username but not an email.
        response = client.post(
            '/auth/users/create/',
            {
                'username': 'tester1',
                'password': 'Password01'
            },
            format='json'
        )
        self.assertEquals(400, response.status_code)
        self.assertIn('This field is required.', response.data['email'])

        # User then tries to create user with an email and not a username
        response = client.post(
            '/auth/users/create/',
            {
                'email': 'testing@mail.com',
                'password': 'Password01'
            },
            format='json'
        )
        self.assertEquals(201, response.status_code)
        self.assertIn('testing@mail.com', response.data['email'])

        self.fail("End Testing")
        # User gets the registration email from their mailbox
        email = mail.outbox[0]
        uid = "xyz"
        token = "abc"
        # Figure out how to parse email, exfiltrate the code for registration
        response = client.post(
            '/auth/users/activate/',
            {
                'uid': uid,
                'token': token
            },
            format='json'
        )

        # REST Call to register endpoint
        # Intercept the register email, get the reigster token
        # Enter the register token in a page
        # Once registered, user needs to log in
        # REST Call to the Login endpoint
        # returns a JWT for authorisation
        # Ensure a call to the user endpoint using the JWT will return details.
        # Make call to the user endpoint to add user details.
        # User cannot see the personal details of user created during setup and teardown
    
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

import re

from django.core import mail
from django.test.utils import override_settings

from .base import FunctionalRestTest


class AuthFunctionalTests(FunctionalRestTest):

    def test_user_can_register_and_login(self):
        user = {
            'email': 'testing@mail.com',
            'name': 'Tester01',
            'password': 'Password01'
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
        uid, token = self.get_uid_and_token_from_email(
            '#\/activate\/(.*?)\/(.*?)\\n', 0)

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

        # User can use the new JWT to make a series of authenticateds
        # requests, such as the user endpoint
        self.check_me_endpoint(user['name'], user['jwt'])

    def test_user_can_change_password(self):
        user_details = self.create_user()

        # Pre-existing user logs in by asking for a JWT
        self.authenticate(user_details)

        # User wants to change their password, so they
        # call the password change endpoint.
        new_password = 'Password02'
        response = self.client.post(
            '/auth/password/',
            {
                "new_password": new_password,
                "re_new_password": new_password,
                "current_password": user_details['password']
            },
            format='json'
        )
        self.assertEquals(204, response.status_code)

        # Once complete, user ensures the old password no longer works
        self.authenticate()
        response = self.create_jwt(
            user_details['email'], user_details['password'])
        self.assertEquals(400, response.status_code)
        self.assertNotIn('token', response.data)

        # User logs in with their new password.
        user_details['password'] = new_password
        response = self.create_jwt(
            user_details['email'],
            user_details['password'])
        self.assertEquals(200, response.status_code)
        self.assertIn('token', response.data)
        user_details['jwt'] = response.data['token']

        # User gets their profile information
        self.check_me_endpoint(user_details['name'], user_details['jwt'])

    def test_user_can_reset_password(self):
        user_details = self.create_user()

        # User makes call to the forgotten password endpoint
        response = self.client.post(
            '/auth/password/reset/',
            {'email': user_details['email']}
        )
        self.assertEqual(204, response.status_code)

        # User retrieves the email from their inbox.
        uid, token = self.get_uid_and_token_from_email(
            '#\/password\/reset\/confirm\/(.*?)\/(.*?)\\n', 0)

        # User makes call to the reset confirm endpoint
        # with uid, token and new password
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
        response = self.create_jwt(
            user_details['email'], user_details['password'])
        self.assertEqual(400, response.status_code)
        self.assertNotIn('token', response.data)

        # User can now create a JWT with the new password
        response = self.create_jwt(user_details['email'], new_password)
        self.assertEqual(200, response.status_code)
        self.assertIn('token', response.data)
        user_details['jwt'] = response.data['token']

        # User can now see their details with the created JWT.
        self.check_me_endpoint(user_details['name'], user_details['jwt'])

    def test_user_can_change_email_address(self):
        user_details = self.create_user()
        self.authenticate(user_details)

        # User posts to the change email address endpoint
        new_email = 'test2@mail.com'
        response = self.client.post(
            '/auth/email/',
            {
                "current_password": user_details['password'],
                "new_email": new_email,
                "re_new_email": new_email
            },
            format='json'
        )
        self.assertEqual(204, response.status_code)

        # User gets the UID and Token from the activation email
        self.authenticate()
        uid, token = self.get_uid_and_token_from_email(
            '#\/activate\/(.*?)\/(.*?)\\n', 0)
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
        response = self.create_jwt(
            user_details['email'], user_details['password'])
        self.assertEqual(400, response.status_code)
        self.assertNotIn('token', response.data)

        # User can log in with new email address.
        response = self.create_jwt(new_email, user_details['password'])
        self.assertEqual(200, response.status_code)
        self.assertIn('token', response.data)

    def test_can_refresh_and_verify_jwt(self):
        user_details = self.create_user()
        
        # Existing User logs in by creating new JWT.
        response = self.create_jwt(
            user_details['email'], user_details['password'])
        self.assertEqual(200, response.status_code)
        self.assertIn('token', response.data)
        user_details['jwt'] = response.data['token']

        # User verify's the JWT that was created.
        response = self.client.post(
            '/auth/jwt/verify/',
            {
                "token": user_details['jwt']
            },
            format="json"
        )
        self.assertEqual(200, response.status_code)

        # Change JWT payload by one char, verify should now not work.
        invalid_jwt = user_details['jwt'][:-1]
        response = self.client.post(
            '/auth/jwt/verify/',
            {
                "token": invalid_jwt
            },
            format="json"
        )
        self.assertEqual(400, response.status_code)

        # User can then refresh originally generated JWT.
        response = self.client.post(
            '/auth/jwt/refresh/',
            {
                "token": user_details['jwt']
            },
            format="json"
        )
        self.assertEqual(200, response.status_code)
        self.assertIn('token', response.data)
        user_details['jwt'] = response.data['token']

        # User can see the me endpoint with newly refresh JWT!
        self.check_me_endpoint(user_details['name'], user_details['jwt'])

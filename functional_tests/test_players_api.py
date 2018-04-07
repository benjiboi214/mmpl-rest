from .base import FunctionalRestTest


class StaffUserFunctionalTests(FunctionalRestTest):

    def test_player_list_endpoint(self):
        staff_details = self.create_staff_user()
        self.authenticate(staff_details)

        # Staff user can POST list view
        response = self.client.post(
            '/players/',
            {
                'name': 'Ben Elliot',
            },
            format='json'
        )
        self.assertEqual(201, response.status_code)

        # Staff user can GET list view
        response = self.client.get(
            '/players/',
            format='json'
        )
        self.assertEqual(200, response.status_code)

    def test_player_detail_endpoint(self):
        user_details = self.create_user()
        staff_details = self.create_staff_user()
        self.authenticate(staff_details)

        # Staff user can GET
        response = self.client.get(
            '/players/' + self.user.profile.uuid.__str__() + '/',
            format='json'
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            self.user.profile.uuid.__str__(),
            response.data['uuid'])

        # Staff user can PUT
        response = self.client.put(
            '/players/' + self.user.profile.uuid.__str__() + '/',
            {
                'name': user_details['name']
            },
            format='json'
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(user_details['name'], response.data['name'])

        # Staff user can DELETE
        response = self.client.delete(
            '/players/' + self.user.profile.uuid.__str__() + '/',
            format='json'
        )
        self.assertEqual(204, response.status_code)

        # Staff user cannot POST
        response = self.client.post(
            '/players/' + self.user.profile.uuid.__str__() + '/',
            format='json'
        )
        self.assertEqual(405, response.status_code)


class AuthenticatedUserFunctionalTests(FunctionalRestTest):

    def test_player_list_endpoint(self):
        user_details = self.create_user()
        self.authenticate(user_details)

        # Authenticated user cannot POST the list view
        response = self.client.post(
            '/players/',
            {
                'name': 'Ben Elliot',
            },
            format='json'
        )
        self.assertEqual(403, response.status_code)

        # Authenticated user can GET list view
        response = self.client.get(
            '/players/',
            format='json'
        )
        self.assertEqual(200, response.status_code)

    def test_player_me_endpoint(self):
        user_details = self.create_user()
        self.authenticate(user_details)

        # User has access to their player profile.
        response = self.client.get(
            '/players/me/',
            format='json'
        )
        self.assertEqual(200, response.status_code)
        self.assertIn('uuid', response.data)

        # User can post and update the address on their profile
        response = self.client.put(
            '/players/me/',
            {
                'name': 'Ben Elliot',
                'address': '123 Fake Street, Melbourne',
                'date_of_birth': '1992-04-21',
                'phone_number': '0429 227 281',
                'umpire_accreditation': 'A'
            },
            format='json'
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual('Ben Elliot', response.data['name'])

    def test_player_detail_endpoint(self):
        user_details = self.create_user()
        other_user_details = self.create_other_user()
        self.authenticate(user_details)

        # Authenticated User can GET
        response = self.client.get(
            '/players/' + self.user.profile.uuid.__str__() + '/',
            format='json'
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            self.user.profile.uuid.__str__(),
            response.data['uuid'])

        # Authenticated User can PUT their own resource
        new_name = 'New User Name'
        response = self.client.put(
            '/players/' + self.user.profile.uuid.__str__() + '/',
            {
                'name': new_name
            },
            format='json'
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(new_name, response.data['name'])

        # Authenticated User cannot PUT another resource
        response = self.client.put(
            '/players/' + self.other_user.profile.uuid.__str__() + '/',
            {
                'name': new_name
            },
            format='json'
        )
        self.assertEqual(403, response.status_code)

        # Authenticated User canot DELETE
        response = self.client.delete(
            '/players/' + self.user.profile.uuid.__str__() + '/',
            format='json'
        )
        self.assertEqual(403, response.status_code)


class AnonUserFunctionalTests(FunctionalRestTest):

    def test_player_list_endpoint(self):
        self.create_user()

        # Unauthenticaed user can GET the list view
        response = self.client.get(
            '/players/',
            format='json'
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.created_profiles, len(response.data))

        # Unauthenticated user cannot POST the list view
        response = self.client.post(
            '/players/',
            {
                'name': 'Ben Elliot',
            },
            format='json'
        )
        self.assertEqual(401, response.status_code)

    def test_player_me_endpoint(self):
        # User has no access to a player profile.
        response = self.client.get(
            '/players/me/',
            format='json'
        )
        self.assertEqual(401, response.status_code)

    def test_player_detail_endpoint(self):
        user_details = self.create_user()

        # Anonymous user can GET
        response = self.client.get(
            '/players/' + self.user.profile.uuid.__str__() + '/',
            format='json'
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            self.user.profile.uuid.__str__(),
            response.data['uuid'])

        # Anonymous user cannot PUT
        response = self.client.put(
            '/players/' + self.user.profile.uuid.__str__() + '/',
            {
                'name': 'New Value'
            },
            format='json'
        )
        self.assertEqual(401, response.status_code)

        # Anonymous user cannot DELETE
        response = self.client.delete(
            '/players/' + self.user.profile.uuid.__str__() + '/',
            format='json'
        )
        self.assertEqual(401, response.status_code)


# Admin should get a list of claims irrespective of players /players/claims/
# Admin should be able to select specific request to get detail and verify. /players/claims/<uuid>/
#
# User should have a claim action on a profile-detail /players/<uuid>/claim
# User should have a /players/claims/ endpoint to show their claims
# For above if authenticated, return array, empty or not.
#
# Anon user should see none of the above.



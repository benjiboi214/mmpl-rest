# User can edit, update and otherwise change their player profile.
# User cannot edit another players profile.
# If a profile exists without an associated profile, player can claim the profile
# Admin should recieve confirmation that profile has been claimed awaiting approval.
# User can input details such as contact details, preferred contact method, address, umpire accreditation.
# User can enter a preferred Name (screen name?)

from .base import FunctionalRestTest


class PlayerFunctionalTests(FunctionalRestTest):

    def test_player_profile_can_be_edited(self):
        # User logs in
        response = self.create_jwt(
            self.other_user['email'], self.other_user['password'])
        self.other_user['jwt'] = response.data['token']
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT ' + self.other_user['jwt'])

        # Once logged in, user has access to their
        # player profile and can see that it is empty.
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
                'address': '123 Fake Street, Melbourne',
                'date_of_birth': '1992-04-21',
                'phone_number': '0429 227 281',
                'umpire_accreditation': 'A'
            },
            format='json'
        )

        # Unauthenticated user cannot access same endpoint.

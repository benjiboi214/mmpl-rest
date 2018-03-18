# If a profile exists without an associated profile, player can claim the profile
# Admin should recieve confirmation that profile has been claimed awaiting approval.
# User can input details such as contact details, preferred contact method, address, umpire accreditation.

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

        # Unauthenticated user cannot access same endpoint.
        self.client.credentials()
        response = self.client.get(
            '/players/me/',
            format='json'
        )
        self.assertEqual(401, response.status_code)

    def test_player_profile_list(self):
        # Unauthenticaed user can GET the list view
        response = self.client.get(
            '/players/',
            format='json'
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))

        # Unauthenticated user cannot POST the list view
        response = self.client.post(
            '/players/',
            {
                'name': 'Ben Elliot',
            },
            format='json'
        )
        self.assertEqual(401, response.status_code)

        # Authenticated user cannot POST the list view
        response = self.create_jwt(
            self.other_user['email'], self.other_user['password'])
        self.other_user['jwt'] = response.data['token']
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT ' + self.other_user['jwt'])

        response = self.client.post(
            '/players/',
            {
                'name': 'Ben Elliot',
            },
            format='json'
        )
        self.assertEqual(403, response.status_code)

        # Authenticated Admin user can POST list view
        response = self.create_jwt(
            self.admin_user['email'], self.admin_user['password'])
        self.admin_user['jwt'] = response.data['token']
        self.client.credentials(
            HTTP_AUTHORIZATION='JWT ' + self.admin_user['jwt'])

        response = self.client.post(
            '/players/',
            {
                'name': 'Ben Elliot',
            },
            format='json'
        )
        self.assertEqual(201, response.status_code)


### Test Cases for Profile Request Track ###
# Profile is created by external process (no user attached)
# User navigates to profile making get request on player resource
# /players/{uuid}/
# Player notices that the profile is theirs, makes post request to /claim endpoint
# /players/{uuid}/claim (Authenticated)
# claim endpoint takes the profile, the user and creates an intermediary model ProfileClaim
# Message posted to the user that the request has been filed

# On ProfileClaim creation, admin gets an email asking for approval of the claim
# Admin navigates to /players/claims/{uuid} (Admin permissions)
# Admin can see the which user has claimed which profile
# Admin can check the verification code to confirm the right human has claimed the right profile.

# If the code is correct, admin posts to /players/claims/{uuid}/approve (Admin only permissions)
# Internally, take the User and Profile and link
# Remove request model.
# Notify User their request was approved.

# If the code in not correct, admin posts to /players/claims/{uuid}/decline (Admin only permissions)
# Internally, remove the ProfileClaim
# Notify User their request was declined.

# ProfileClaim Model
# user = OneToOne with User
# profile = OneToOne with Profile
# code = UUID Field for verification
# (M) = Approve
# (M) = Decline

from .base import FunctionalRestTest
from userprofile.models import Profile, Claim
from django.contrib.auth import get_user_model


class ClaimRestTest(FunctionalRestTest):

    def setUp(self):
        super(ClaimRestTest, self).setUp()
        self.created_claims = 0
        self.unpaired_user = 0

    def create_unpaired_user(self):
        self.unpaired_user += 1
        unpaired_user_details = {
            'email': f'unpaired{self.unpaired_user}@mail.com'
        }
        user = get_user_model().objects.create(
            email=unpaired_user_details['email']
        )
        user.save()
        return user

    def create_profile(self):
        profile = Profile.objects.create()
        profile.save()
        self.created_profiles += 1
        return profile

    def create_claim(self, user, profile):
        claim = Claim.objects.create(profile=profile, user=user)
        claim.save()
        self.created_claims += 1
        return claim


class StaffUserFunctionalTests(ClaimRestTest):

    def test_player_claim_list_endpoint(self):
        # Admin should see full list of claims
        self.create_claim(self.create_unpaired_user(), self.create_profile())
        staff_details = self.create_staff_user()
        self.authenticate(staff_details)

        response = self.client.get(
            '/players/claims/',
            format='json'
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.created_claims, len(response.data))

    def test_player_claim_detail_endpoint(self):
        # Admin should be able to open claim details
        pass

    def test_player_claim_action_endpoint(self):
        # Admin should be able to claim a profile if required.
        pass


class AuthenticatedUserFunctionalTests(ClaimRestTest):

    def test_player_claim_list_endpoint(self):
        # User should be able to use the claim list, but only return their claimed profile.
        user_details = self.create_user()
        self.create_claim(self.create_unpaired_user(), self.user.profile)
        self.create_claim(self.create_unpaired_user(), self.create_profile())
        self.authenticate(user_details)

        response = self.client.get(
            '/players/claims/',
            format='json'
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))

    def test_player_claim_detail_endpoint(self):
        # Authenticated user should not see this endpoint.
        pass

    def test_player_claim_action_endpoint(self):
        # Authenticated user should be able to claim a profile.
        pass


class AnonUserFunctionalTests(ClaimRestTest):

    def test_player_claim_list_endpoint(self):
        # Anon user should not see the claim list
        self.create_claim(self.create_unpaired_user(), self.create_profile())
        self.create_claim(self.create_unpaired_user(), self.create_profile())

        response = self.client.get(
            '/players/claims/',
            format='json'
        )
        self.assertEqual(401, response.status_code)

    def test_player_claim_detail_endpoint(self):
        # Anon user should not see the claim detail
        pass

    def test_player_claim_action_endpoint(self):
        # Anon user should not be able to use the claim action.
        pass

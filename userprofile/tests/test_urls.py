from django.test import TestCase
from django.urls import reverse, resolve


class ProfileUrlTest(TestCase):

    def test_player_me_url_resolves_to_correct_path(self):
        url = reverse('player_me_detail')
        self.assertEqual(url, '/players/me/')

    def test_player_me_url_resolves_correct_view(self):
        resolver = resolve('/players/me/')
        self.assertEqual(resolver.view_name, 'player_me_detail')
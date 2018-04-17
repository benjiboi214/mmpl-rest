from django.test import TestCase
from django.urls import resolve, reverse


class ProfileUrlTest(TestCase):

    def test_player_me_url_resolves_to_correct_path(self):
        url = reverse('profile-me')
        self.assertEqual(url, '/players/me/')

    def test_player_me_url_resolves_correct_view(self):
        resolver = resolve('/players/me/')
        self.assertEqual(resolver.view_name, 'profile-me')

    def test_player_list_url_resolves_correct_path(self):
        url = reverse('profile-list')
        self.assertEqual(url, '/players/')

    def test_player_list_url_resolves_correct_view(self):
        resolver = resolve('/players/')
        self.assertEqual(resolver.view_name, 'profile-list')

    def test_player_detail_url_resolves_correct_path(self):
        url = reverse('profile-detail', args=['ABCDEFGHIJKLMNOP'])
        self.assertEqual(url, '/players/ABCDEFGHIJKLMNOP/')

    def test_player_detail_url_resolves_correct_view(self):
        resolver = resolve('/players/ABCDEFGHIJKLMNOP/')
        self.assertEqual(resolver.view_name, 'profile-detail')

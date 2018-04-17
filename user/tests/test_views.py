from django.test import TestCase


# Create your tests here.
class DeleteViewTest(TestCase):

    def test_returns_404(self):
        response = self.client.get('/auth/users/delete/')
        self.assertEqual(404, response.status_code)

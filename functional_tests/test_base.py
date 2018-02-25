from selenium import webdriver
import time
from django.test.utils import override_settings

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

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

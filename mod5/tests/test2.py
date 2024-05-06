import unittest
from hw2 import app

class TestFlask(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.base_url = 'https://localhost/run_code'

    def test_timeout(self):
        response = self.app.post(self.base_url, data={"code": "import time; time.sleep(2)", "timeout": 4})
        self.assertTrue(response.status_code == 200)

    def test_with_wrong_timeout(self):
        response = self.app.post(self.base_url, data={"code": "import time; time.sleep(2)", "timeout": "two"})
        self.assertTrue(response.status_code == 400)

    def test_with_wrong_big_timeout(self):
        response = self.app.post(self.base_url, data={"code": "import time; time.sleep(2)", "timeout": 31})
        self.assertTrue(response.status_code == 400)

    def test_shell(self):
        response = self.app.post(self.base_url, data={"code": 'print()"; echo "hacked', "timeout": 1})
        self.assertTrue('hacked' not in response.text)
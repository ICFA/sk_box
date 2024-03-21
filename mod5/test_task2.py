import unittest
from task2 import app

class TestFlask(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.base_url = 'https://localhost/run_code'

    def test_timeout(self):
        response = self.app.post(self.base_url, data={"code": "import time; time.sleep(2)", "timeout": 1})
        assert (response.text.split(": ")[-1] == "True")

    def test_with_wrong_timeout(self):
        response = self.app.post(self.base_url, data={"code": "import time; time.sleep(2)", "timeout": "two"})
        assert (response.status_code == 400)

    def test_with_wrong_big_timeout(self):
        response = self.app.post(self.base_url, data={"code": "import time; time.sleep(2)", "timeout": 31})
        assert (response.status_code == 400)

    def test_shell(self):
        response = self.app.post(self.base_url, data={"code": 'print()"; echo "hacked', "timeout": 1})
        assert ('hacked' not in response.text)
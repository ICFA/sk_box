import unittest
from registration import app


class TestRegistration(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()
        self.base_url = '/registration'
        self.data = {
            "email": "test@example.com",
            "phone": 9999999999,
            "name": "Nikita",
            "address": "Ekaterinburg",
            "index": 1,
            "comment": "Im Nikita"
        }

    # email
    def test_wrong_email(self):
        self.data['email'] = 'test@ex'
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

        self.data['email'] = 123456
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_wrong_phone(self):
        self.data['phone'] = 'phone'
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

        self.data['phone'] = 99999999999999
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

        self.data['phone'] = 9
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_empty_email(self):
        self.data.pop('email', None)
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_wrong_index(self):
        self.data['index'] = 'index'
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_empty_phone(self):
        self.data.pop('phone', None)
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_empty_name(self):
        self.data.pop('name', None)
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_empty_address(self):
        self.data.pop('phone', None)
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_empty_index(self):
        self.data.pop('index', None)
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_run_app(self):
        response = self.app.post(self.base_url, data=self.data)
        self.assertEqual(response.status_code, 200)
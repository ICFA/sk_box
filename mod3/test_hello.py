import unittest
from mod2.task4_7 import app, weekdays
from freezegun import freeze_time
from datetime import datetime


class TestHellWorldApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    @freeze_time("2024-03-14")
    def test_get_correct_username_with_weekday(self):
        username = 'username'
        excepted_weekday = 3
        weekday = datetime.now().weekday()
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue(username in response_text)
        self.assertEqual(weekdays[excepted_weekday], weekdays[weekday])

    def test_all_weekdays(self):
        username = 'username'
        for i in range(11, 18):
            date = f"2024-03-{i}"
            excepted_weekday = i - 11
            with freeze_time(date):
                weekday = datetime.now().weekday()
                response_text = self.app.get(self.base_url + username).data.decode()
                self.assertTrue(username in response_text)
                self.assertEqual(excepted_weekday, weekday)

    @freeze_time("2024-03-14")
    def test_good_day_in_username(self):
        username = "Хорошей субботы"
        excepted_weekday = 3
        weekday = datetime.now().weekday()
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue(username in response_text)
        self.assertEqual(weekdays[excepted_weekday], weekdays[weekday])
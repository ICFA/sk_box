import unittest
from mod2.task4_7 import app, storage

storage_test = {2024: {
                        1: {
                            1: 10,
                            2: 20,
                            'total': 30
                        },
                        'total': 30
                         }
                    }

class TestFinanceFlaskApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        cls.app = app.test_client()
        storage.update(storage_test)

    def test_get_correct_add(self):
        date = '20211212'
        expense = 10
        new_spend = (2021, {12: {12: 10, 'total': 10}, 'total': 10})

        self.app.get('/add/' + date + f'/{expense}')
        self.assertTrue(new_spend in storage.items())

    def test_add_with_wrong_date(self):
        wrong_date = 1
        expense = 1

        with self.assertRaises(ValueError):
            self.app.get('/add/' + f'{wrong_date}/{expense}')


    def test_calculate_year(self):
        year = 2024
        response_text = self.app.get('/calculate/' + str(year)).data.decode()
        self.assertTrue(str(storage[year]['total']) in response_text)

    def test_empty_storage_in_calculate_year(self):
        storage.clear()
        year_not_in_storage = 2000
        with self.assertRaises(KeyError):
            self.app.get('/calculate/' + str(year_not_in_storage))

    def test_calculate_year_and_month(self):
        year = 2024
        month = 1
        response_text = self.app.get('/calculate/' + f'{year}/{month}').data.decode()
        self.assertTrue(str(storage[year][month]['total']) in response_text)

    def test_empty_storage_in_calculate(self):
        storage.clear()
        year_not_in_storage = 2000
        month_not_in_storage = 9
        with self.assertRaises(KeyError):
            self.app.get('/calculate/' + f'{year_not_in_storage}/{month_not_in_storage}')
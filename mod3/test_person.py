import unittest
from mod3.person import Person
from datetime import datetime

person = Person('Nikita', 2004, 'Yekaterinburg, Lenina, 13')

class TestPerson(unittest.TestCase):

    def test_can_get_age(self):
        expected_age = datetime.now().year - 2004
        person_age = person.get_age()
        self.assertEqual(expected_age, person_age)

    def test_can_get_name(self):
        expected_name = 'Nikita'
        person_name = person.get_name()
        self.assertEqual(expected_name, person_name)

    def test_can_get_address(self):
        expected_address = 'Yekaterinburg, Lenina, 13'
        person_address = person.get_address()

        self.assertEqual(expected_address, person_address)

    def test_is_not_homeless(self):
        expected_homeless = False
        person_homeless = person.is_homeless()
        self.assertEqual(expected_homeless, person_homeless)

    def test_is_homeless(self):
        homeless_person = Person('Lala', 1999, None)
        expected_homeless = True
        person_homeless = homeless_person.is_homeless()
        self.assertEqual(expected_homeless, person_homeless)

    def test_can_set_name(self):
        expected_name = 'Lala'
        person.set_name('Lala')
        person_name = person.get_name()

        self.assertEqual(expected_name, person_name)

    def test_can_set_address(self):
        expected_address = 'Moscow, Lenina, 13'
        person.set_address('Moscow, Lenina, 13')
        person_address = person.get_address()

        self.assertEqual(expected_address, person_address)

    def test_can_not_set_wrong_age(self):
        with self.assertRaises(ValueError):
            Person('Nikita', 300000, 'Moscow, Lenina, 13')


if __name__ == '__main__':
    unittest.main()
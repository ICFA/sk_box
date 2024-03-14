from mod2.task3 import decrypt
import unittest


phrases_result_one = ['абра-кадабра.', 'абраа..-кадабра', 'абраа..-.кадабра', 'абра--..кадабра', 'абрау...-кадабра']
phrases_result_empty = ['абра........', '.', '1.......................']

class TestDecrypt(unittest.TestCase):
    def test_get_one_phrases(self):
        for phrases in phrases_result_one:
            with self.subTest(phrases=phrases):
                self.assertEqual(decrypt(phrases), 'абра-кадабра')

    def test_get_empty(self):
        for phrases in phrases_result_empty:
            with self.subTest(phrases=phrases):
                self.assertEqual(decrypt(phrases), '')

    def test_get_numbers_23(self):
        self.assertEqual(decrypt('1..2.3'), '23')

    def test_get_letter_a(self):
        self.assertEqual(decrypt('абр......a.'), 'a')


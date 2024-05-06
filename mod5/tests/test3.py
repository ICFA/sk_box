import unittest
from hw3 import BlockErrors

class TestBlockErrors(unittest.TestCase):
    def test_div_to_zero(self):
        try:
            err_types = {ZeroDivisionError, TypeError}
            with BlockErrors(err_types):
                a = 1 / 0
            print('Выполнено без ошибок')
            assert (True)
        except: assert(False)

    def test_div_to_string_zero(self):
        try:
            err_types = {ZeroDivisionError}
            with BlockErrors(err_types):
                a = 1 / '0'
            print('Выполнено без ошибок')
            assert (False)
        except: assert(True)

    def test_inner_block(self):
        try:
            outer_err_types = {TypeError}
            with BlockErrors(outer_err_types):
                inner_err_types = {ZeroDivisionError}
                with BlockErrors(inner_err_types):
                    a = 1 / '0'
                print('Внутренний блок: выполнено без ошибок')
            print('Внешний блок: выполнено без ошибок')
            assert (True)
        except: assert(False)

    def test_daughter_error(self):
        try:
            err_types = {Exception}
            with BlockErrors(err_types):
                a = 1 / '0'
            print('Выполнено без ошибок')
            assert (True)
        except: assert(False)
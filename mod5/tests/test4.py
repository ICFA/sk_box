import unittest
from hw4 import Redirect

class TestRedirect(unittest.TestCase):
    def test_stdout_file(self):
        stdout_file = open('../stdout.txt', 'w')
        stderr_file = open('../stderr.txt', 'w')
        with Redirect(stdout=stdout_file, stderr=stderr_file):
            print('Hello stdout.txt')
            raise Exception('Hello stderr.txt')

        stdout_file = open('../stdout.txt')
        assert('Hello stdout.txt' in stdout_file.read())

    def test_stderr_file(self):
        stdout_file = open('../stdout.txt', 'w')
        stderr_file = open('../stderr.txt', 'w')
        with Redirect(stdout=stdout_file, stderr=stderr_file):
            print('Hello stdout.txt')
            raise Exception('Hello stderr.txt')

        stderr_file = open('../stderr.txt')
        assert ("Traceback (most recent call last):" in stderr_file.read())
from datetime import datetime

class Person:

    def __init__(self, name, year_of_birth, address=''):
        self.name = name
        self.address = address

        if year_of_birth <= datetime.now().year:
            self.yob = year_of_birth
        else:
            raise ValueError('Wrong age')

    def get_age(self):
        now = datetime.now()
        return now.year - self.yob

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def set_address(self, address):
        self.address = address

    def get_address(self):
        return self.address

    def is_homeless(self):
        return self.address is None
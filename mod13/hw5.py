import random
import sqlite3
import string

countries = ['Германия', 'Португалия', 'Бельгия', 'Испания', 'Франция', 'Англия', 'Швейцария', 'Италия', 'Польша', 'Исландия']
categories = ['Сильная команда', 'Средняя команда', 'Средняя команда', 'Слабая команда']

sql_commands = """
INSERT INTO uefa_commands (id, name, country, category) VALUES (?, ?, ?, ?)
"""

sql_groups = """
INSERT INTO uefa_draw (id, group) VALUES (?, ?)
"""

def generate_test_data(
        c: sqlite3.Cursor,
        number_of_groups: int
) -> None:
    for i in range(number_of_groups * 4):
        id, group = i + 1, i % 4 + 1
        name = random.choice(string.ascii_letters) + str(id)
        country = random.choice(countries)
        category = categories[i % 4]

        cursor.execute(sql_commands, (id, name, country, category))
        cursor.execute(sql_groups, (id, group))


if __name__ == "__main__":
    with sqlite3.connect("../hw.db") as conn:
        cursor = conn.cursor()
        generate_test_data(cursor, int(input()))
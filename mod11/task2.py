import requests
import sqlite3
import time
import threading


LOCK = threading.Lock()

create_table = """
DROP TABLE IF EXISTS `persons`;

CREATE TABLE `persons` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    height INTEGER NOT NULL,
    birth_year VARCHAR NOT NULL,
    gender VARCHAR NOT NULL
);
"""


def consequent_request():
    records = []
    person = {}
    for i in range(1, 22):
        try:
            r = requests.get(f'https://swapi.dev/api/people/{i}')
            person = r.json()
            records.append(tuple([person['name'], person['height'], person['birth_year'], person['gender']]))
        except Exception as e:
            print(f"Error fetching data for person {i}: {e}")

    for record in records:
        cur.execute("""INSERT INTO `persons` (name, height, birth_year, gender) VALUES (?, ?, ?, ?)""", record)

def threading_request():
    records = []
    with LOCK:
        for i in range(1, 22):
            try:
                r = requests.get(f'https://swapi.dev/api/people/{i}')
                person = r.json()
                records.append(tuple([person['name'], person['height'], person['birth_year'], person['gender']]))
            except Exception as e:
                print(f"Error fetching data for person {i}: {e}")

        for record in records:
            cur.execute("""INSERT INTO `persons` (name, height, birth_year, gender) VALUES (?, ?, ?, ?)""", record)


if __name__ == "__main__":
    with sqlite3.connect("star_wars.db") as conn:
        cur = conn.cursor()
        cur.executescript(create_table)  # Выполнение SQL-запросов для создания таблицы
        start_time1 = time.time()
        consequent_request()
        end_time1 = time.time()
        conn.commit()  # Сохранение изменений в базе данных
        execution_time1 = end_time1 - start_time1
        print('conseq', execution_time1)
        start_time2 = time.time()
        threading_request()
        end_time2 = time.time()
        execution_time2= end_time2 - start_time2
        print('threading', execution_time2)
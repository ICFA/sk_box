import requests
import sqlite3
import time
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool

create_table = """
CREATE TABLE `persons` (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    height INTEGER NOT NULL,
    birth_year VARCHAR NOT NULL,
    gender VARCHAR NOT NULL
);
"""

def fetch_person_data(person_id):
    try:
        r = requests.get(f'https://swapi.dev/api/people/{person_id}')
        person = r.json()
        return tuple([person['name'], person['height'], person['birth_year'], person['gender']])
    except Exception as e:
        print(f"Error fetching data for person {person_id}: {e}")
        return None


def multiprocessing_request():
    num_workers = 4
    with sqlite3.connect("star_wars.db") as conn:
        cur = conn.cursor()
        cur.executescript(create_table)

        with Pool(num_workers) as pool:
            records = pool.map(fetch_person_data, range(1, 22))
            valid_records = [record for record in records if record is not None]

            cur.executemany(
                """INSERT INTO `persons` (name, height, birth_year, gender) 
                         VALUES (?, ?, ?, ?)""",
                valid_records
            )
            conn.commit()


def threadpool_request():
    num_workers = 4
    with sqlite3.connect("star_wars.db") as conn:
        cur = conn.cursor()
        cur.executescript(create_table)

        with ThreadPool(num_workers) as pool:
            records = pool.map(fetch_person_data, range(1, 22))
            valid_records = [record for record in records if record is not None]

            cur.executemany(
                """INSERT INTO `persons` (name, height, birth_year, gender) 
                         VALUES (?, ?, ?, ?)""",
                valid_records
            )
            conn.commit()


if __name__ == "__main__":
    start_time1 = time.time()
    multiprocessing_request()
    end_time1 = time.time()
    execution_time1 = end_time1 - start_time1
    print(execution_time1)

    start_time2 = time.time()
    threadpool_request()
    end_time2 = time.time()
    execution_time2 = end_time2 - start_time2
    print(execution_time2)
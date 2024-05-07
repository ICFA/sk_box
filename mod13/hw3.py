import sqlite3

def log_bird(cursor: sqlite3.Cursor, bird_name: str, date_time: str,) -> None:
    cursor.execute(f"INSERT INTO 'birds' (bird_name, date_time) "
                   f"VALUES ('{bird_name}', '{date_time}');")


def check_if_such_bird_already_seen(cursor: sqlite3.Cursor, bird_name: str) -> bool:
    cursor.execute(f"SELECT COUNT(*) FROM 'birds' "
                   f"WHERE bird_name = '{bird_name}'")
    result = cursor.fetchone()[0]
    return True if result >= 1 else False


if __name__ == '__main__':
    name = input("Имя птицы: ").lower()
    date = input("Дата обнаружения: ")

    with sqlite3.connect('bird.db') as conn:
        cursor = conn.cursor()
        log_bird(cursor, name, date)
        print(check_if_such_bird_already_seen(cursor, name))
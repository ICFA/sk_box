import sqlite3

get_sql = """
SELECT * FROM 'table_effective_manager'
WHERE name = ?"""

update_sql = """
UPDATE 'table_effective_manager'
SET salary = ?
WHERE name = ?
"""

delete_sql = """
DELETE
FROM 'table_effective_manager'
WHERE name = ?
"""

def ivan_sovin_the_most_effective(cursor: sqlite3.Cursor, name: str,):
    cursor.execute(get_sql, (name,))
    salary = cursor.fetchone()[0]
    if name == "Иван Совин":
        return

    if salary * 1.1 <= sovin:
        cursor.execute(update_sql, (salary * 1.1, name))
    else:
        cursor.execute(delete_sql, (name,))



if __name__ == '__main__':
    with sqlite3.connect('../hw.db') as conn:
        cursor = conn.cursor()
        cursor.execute(get_sql, "Иван Совин")
        sovin, *_ = cursor.fetchone()
        print(ivan_sovin_the_most_effective(cursor, 'Иван Совин'))
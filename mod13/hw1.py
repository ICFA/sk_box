import sqlite3

sql_request = """
SELECT * FROM 'table_truck_with_vaccine'
WHERE temperature_in_celsius NOT BETWEEN 16 AND 20 AND truck_number = ? 
ORDER BY timestamp
"""

def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str
) -> bool:
    res_checks = cursor.execute(sql_request, (truck_number,)).fetchall()
    if len(res_checks) >= 3:
        print("Spoiled")
        return True
    print("It's ok")
    return False

if __name__ == "__main__":
    with sqlite3.connect("../hw.db") as conn:
        cursor = conn.cursor()
        truck_number = input("Введите номер грузовика:\n")
        check_if_vaccine_has_spoiled(cursor, truck_number)
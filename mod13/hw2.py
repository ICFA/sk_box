import sqlite3
import csv

sql_del = "DELETE FROM table_fees WHERE truck_number = ? and timestamp = ?"


def delete_wrong_fees(cursor: sqlite3.Cursor, wrong_fees_file: str) -> None:
    with open(wrong_fees_file, 'r') as fees:
        for data in csv.reader(fees):
            [cursor.execute(sql_del, numbers) for numbers in data[1:]]



if __name__ == "__main__":
    with sqlite3.connect("../hw.db") as connect:
        cursor: sqlite3.Cursor = connect.cursor()
        delete_wrong_fees(cursor, "../wrong_fees.csv")

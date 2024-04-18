import sqlite3

def count_rows_from_each_table():
    with sqlite3.connect("hw_3_database.db") as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT COUNT(*) FROM 'table_1'").fetchone()[0]
        result += cursor.execute("SELECT COUNT(*) FROM 'table_2'").fetchone()[0]
        result += cursor.execute("SELECT COUNT(*) FROM 'table_3'").fetchone()[0]
        return result

def count_unique_table1():
    with sqlite3.connect("hw_3_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT value) FROM 'table_1'")
        result = cursor.fetchone()[0]
        return result

def count_table1_table2_intersection():
    with sqlite3.connect("hw_3_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM (SELECT value FROM table_1 INTERSECT SELECT value FROM table_2)")
        result = cursor.fetchone()[0]
        return result

def count_all_intersections():
    with sqlite3.connect("hw_3_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM (SELECT value FROM table_1 INTERSECT SELECT value FROM table_2 INTERSECT SELECT value FROM table_3)")
        result = cursor.fetchone()[0]
        return result


print(count_rows_from_each_table())
print(count_unique_table1())
print(count_table1_table2_intersection())
print(count_all_intersections())
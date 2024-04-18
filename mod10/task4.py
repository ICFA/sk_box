import sqlite3

def count_poor():
    with sqlite3.connect("hw_4_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM salaries WHERE salary < 5000")
        result = cursor.fetchone()[0]
        return result

def count_average():
    with sqlite3.connect("hw_4_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(salary) FROM salaries")
        result = cursor.fetchone()[0]
        return result

def count_median():
    with sqlite3.connect("hw_4_database.db") as conn:
        cursor = conn.cursor()
        total = cursor.execute("SELECT COUNT(*) FROM salaries").fetchone()[0]
        result = cursor.execute("SELECT salary FROM salaries ORDER BY salary").fetchall()[total // 2][0]
        return result

def count_disparity():
    with sqlite3.connect("hw_4_database.db") as conn:
        cursor = conn.cursor()
        total = cursor.execute("SELECT SUM(salary) FROM salaries").fetchone()[0]
        t = cursor.execute("SELECT SUM(salary) FROM (SELECT salary FROM salaries ORDER BY salary DESC LIMIT 10)").fetchone()[0]
        f = t / (total - t)
        return round(f, 2)

print(count_poor())
print(count_average())
print(count_median())
print(count_disparity())
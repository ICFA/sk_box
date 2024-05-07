from datetime import datetime, timedelta
import sqlite3

sql_request_drop = """
DELETE FROM table_friendship_schedule
"""

sql_request_get = """
SELECT id, preferable_sport FROM table_friendship_employees
"""

sql_request_insert_employee = """
INSERT INTO table_friendship_schedule (employee_id, date)
VALUES (?,?)
"""

section = ['футбол', "хоккей", "шахматы", "SUP сёрфинг", "бокс", "Dota2", "шах-бокс"]
workers_on_day = {datetime(2020, 1, 1) + timedelta(i): 0 for i in range(366)}
available_dates = list(workers_on_day.keys())

def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    employees = cursor.execute(sql_request_get).fetchall()
    i_day = 0

    # Идея алгоритма: Проходимся по каждому сотруднику и записываем его на ближайшие 10 дней
    # Если в этот день у сотрудника секция - продолжаем запись со след дня
    # Если на этот день записалось 10 человек, то этот день убираем из доступных дат для записи на работы

    # Итого итераций примерно 366 * 10 = 3660 (если быть точнее, то чуть больше)
    for id, preferable_sport in employees:
        working_days_employee = 0
        while working_days_employee <= 10 and len(available_dates) > 0:
            curr_day = available_dates[i_day]

            # Если день уже заполнен 10 людьми
            if workers_on_day[curr_day] == 10:
                workers_on_day.pop(curr_day)
                available_dates.pop(i_day)
                continue

            # Если в этот день нет секции
            if section[curr_day.weekday()] != preferable_sport:
                cursor.execute(sql_request_insert_employee, (id, curr_day))
                working_days_employee += 1
                workers_on_day[curr_day] += 1

            i_day = (i_day + 1) % 366


if __name__ == "__main__":
    with sqlite3.connect("../hw") as conn:
        cursor = conn.cursor()
        cursor.execute(sql_request_drop)
        update_work_schedule(cursor)

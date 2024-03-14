import os
import sys
from flask import Flask
from datetime import datetime

app = Flask(__name__)

#4
weekdays = ('Хорошего понедельника',
            'Хорошего вторника',
            'Хорошей среды',
            'Хорошего четверга',
            'Хорошей пятницы',
            'Хорошей субботы',
            'Хорошего воскресенья')

@app.route('/hello-world/<string:name>')
def hello_world(name):
    weekday = datetime.today().weekday()
    return f'Привет, {name}. {weekdays[weekday]}!'

#5
@app.route("/max_number/<path:numbers>")
def max_number(numbers):
    try:
        numbers_list = [float(i) for i in numbers.split('/')]
        return f'Максимальное число: {max(numbers_list)}'
    except Exception as e:
        return f'Ошибка {type(e).__name__}'

#6
BASE_DIR = os.path.dirname(os.path.abspath('__file__'))

@app.route("/preview/<int:size>/<path:relative_path>")
def preview(size, relative_path):
    abs_path = os.path.join(BASE_DIR, relative_path)

    with open(abs_path, encoding='UTF-8') as file:
        result_text = file.read(size)
        result_size = len(result_text)

    return f'<b>{abs_path}</b> {result_size}<br>{result_text}'

#7

storage = {}

@app.route("/add/<date>/<int:expense>")
def add(date, expense):
    year, month, day = int(date[:4]), int(date[4:6]), int(date[6:])

    storage.setdefault(year, {}).setdefault(month, {}).setdefault(day, 0)
    storage.setdefault(year, {}).setdefault(month, {}).setdefault('total', 0)
    storage.setdefault(year, {}).setdefault('total', 0)

    storage[year][month][day] += expense
    storage[year][month]['total'] += expense
    storage[year]['total'] += expense

    return 'Ваши траты успешно сохранены'

@app.route("/calculate/<int:year>")
def calculate_year(year):
    return f"За {year} год вы потратили {storage[year]['total']}"

@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year, month):
    return f"За {year} год и {month} месяц вы потратили {storage[year][month]['total']}"

    
if __name__ == '__main__':
    app.run(debug=True)
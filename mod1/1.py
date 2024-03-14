import datetime
import os
import random
import re
from functools import wraps
from typing import Callable, Any
from flask import Flask

app = Flask(__name__)

#1
@app.route('/hello_world')
def hello_world():
    return 'Привет, мир!'

#2
cars = ['Chevrolet', 'Renault', 'Ford', 'Lada']

@app.route('/cars')
def car():
    return ', '.join(cars)

#3
cats = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']

@app.route('/cats')
def cat():
    return random.choice(cats)

#4
@app.route('/get_time/now')
def now():
    current_time = datetime.datetime.now()
    return f"Точное время: {current_time}"

#5
@app.route('/get_time/future')
def future():
    current_time_after_hour = datetime.datetime.now() + datetime.timedelta(hours=1)
    return f"Точное время через час будет {current_time_after_hour}"

#6
BASE_DIR = os.path.dirname(os.path.abspath('__file__'))
BOOK_FILE = os.path.join(BASE_DIR, 'for_practice/war_and_peace.txt')

def get_words() -> None:
    global words
    with open(BOOK_FILE, encoding='UTF-8') as book:
        file = ' '.join(book.readlines())
        words = re.findall(r'\b[^0-9 ]\w+', file)

get_words()

@app.route('/get_random_word')
def get_random_word() -> str:
    return random.choice(words)

#7
visits = 0

@app.route('/counter')
def counter(): 
   global visits
   visits += 1
   return str(visits)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
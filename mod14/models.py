import sqlite3
from typing import List, Dict

DATA = [
    {'id': 0, 'title': 'A byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 2, 'title': 'Mar and Peace', 'author': 'Lev Tolstoy'},
]


class Book:
    def __init__(self, title: str, author: str, id=None, views=0):
        self.id = id
        self.title = title
        self.author = author
        self.views = views

    def __getitem__(self, item):
        return getattr(self, item)


def init_db(initial_records: List[Dict]):
    with sqlite3.connect('table_books.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM 'sqlite_master' WHERE type='table' AND name='table_books';")
        exists = cursor.fetchone()
        if not exists:
            exists = cursor.executescript(
                "CREATE TABLE 'table_books' (id INTEGER PRIMARY KEY AUTOINCREMENT, title, author, views)")
            cursor.executemany("INSERT INTO table_books (title, author, views) VALUES (?, ?, 0)",
                               [(item['title'], item['author']) for item in initial_records])


def get_all_books() -> List[Book]:
    with sqlite3.connect("table_books.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * from 'table_books'")
        all_books = cursor.fetchall()
        return [Book(*row) for row in all_books]


# 1
def insert_new_book(book: Book) -> None:
    with sqlite3.connect("table_books.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("INSERT INTO 'table_books' (title, author, views) VALUES (?, ?, 0)", (book.title, book.author))


# 3
def get_books_by_author(author: str) -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("SELECT * from table_books WHERE author = ?", (author,))
        return [Book(*row) for row in cursor.fetchall()]


# 4
def get_book_by_id(id: int) -> Book:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute("UPDATE table_books SET views = views + 1 WHERE id = ?", (id,))
        cursor.execute("SELECT * from table_books WHERE id = ?", (id,))
        return Book(*cursor.fetchone())


if __name__ == '__main__':
    init_db(DATA)

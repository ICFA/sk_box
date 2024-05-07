from typing import List, Dict

from flask import Flask, render_template
from flask import request

from mod14.forms import CreateBookForm, SearchByAuthorForm
from mod14.models import get_all_books, Book, insert_new_book, get_books_by_author, get_book_by_id

app = Flask(__name__)


def _get_hmtl_table_for_books(books: List[Dict]) -> str:
    table = """
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Author</th>
                </tr>
            </thead>
                <tbody>
                    {books_rows}
                </tbody>
        </table>
    """
    rows = ''
    for book in books:
        rows += f'<tr><td>{book['id']}</tb><td>{book['title']}</tb><td>{book['author']}</tb></tr>'
    return table.format(books_rows=rows)


@app.route('/books')
def all_books() -> str:
    return render_template('pred_index.html', books=get_all_books())

#1-2
@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form():
    if request.method == 'GET':
        return render_template('add_book.html')
    if request.method == 'POST':
        form = CreateBookForm()
        book = Book(*form.data)
        insert_new_book(book)
        return 'Книга успешно обавлена'

#3
@app.route('/books/search', methods=['GET', 'POST'])
def search_book_by_author() -> str:
    if request.method == 'GET':
        return render_template('search.html')
    if request.method == 'POST':
        form = SearchByAuthorForm()
        author = form.data['author']
        return render_template('index.html', books=get_books_by_author(author))

#4
@app.route('/books/<id>', methods=['GET'])
def view_book_with_counter(id: int) -> str:
    if request.method == 'GET':
        book = get_book_by_id(id)
        return render_template("details.html", book=book)


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)

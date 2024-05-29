from datetime import datetime, date, timedelta

from flask import Flask, request, jsonify
from sqlalchemy import Column, Integer, Float, String, Boolean, Date, ForeignKey, DateTime, create_engine, func, \
    extract, desc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

app = Flask(__name__)

engine = create_engine('sqlite:///library.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Author(Base):
    """Таблица авторов книг"""
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(100), nullable=False)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Book(Base):
    """Таблица всех книг"""
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    receiving = relationship('ReceivingBook', back_populates='book', cascade="all, delete-orphan", lazy="select")
    students = association_proxy('receiving', 'student')

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ReceivingBook(Base):
    """Таблица выданных книг. Также является промежуточной таблицей между book и students"""
    __tablename__ = 'receiving_books'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)

    date_of_issue = Column(DateTime, default=datetime.now)
    date_of_finish = Column(DateTime, nullable=True)

    book = relationship("Book", back_populates="receiving")
    student = relationship("Student", back_populates="receiving")

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Student(Base):
    """Таблица студентов"""
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    receiving = relationship('ReceivingBook', back_populates='student')
    books = association_proxy('receiving', 'book')


def insert_data():
    authors = [Author(name="Александр", surname="Пушкин"),
               Author(name="Лев", surname="Толстой"),
               Author(name="Михаил", surname="Булгаков")]

    authors[0].books.extend([Book(name="Капитанская дочка", count=5, release_date=date(1836, 1, 1)),
                             Book(name="Евгений Онегин", count=3, release_date=date(1838, 1, 1))])
    authors[1].books.extend([Book(name="Война и мир", count=10, release_date=date(1867, 1, 1)),
                             Book(name="Анна Каренина", count=7, release_date=date(1877, 1, 1))])
    authors[2].books.extend([Book(name="Морфий", count=5, release_date=date(1926, 1, 1)),
                             Book(name="Собачье сердце", count=3, release_date=date(1925, 1, 1))])

    students = [Student(name="Nik", surname="1", phone="2", email="3", average_score=4.5, scholarship=True),
                Student(name="Vlad", surname="1", phone="2", email="3", average_score=4, scholarship=True)]

    session.add_all(authors)
    session.add_all(students)
    session.commit()


@app.before_request
def before_request_func():
    Base.metadata.create_all(bind=engine)
    check_exist = session.query(Author).all()
    if not check_exist:
        insert_data()


@app.route('/books', methods=['GET'])
def all_books():
    """Получение списка всех книг"""
    books = session.query(Book).all()
    # books_r = session.query(ReceivingBook).all()
    books_list = [book.to_json() for book in books]
    return jsonify(books_list=books_list), 200


@app.route('/books/count/<int:author_id>', methods=['GET'])
def count_book_by_author_id(author_id):
    """Получение количества оставшихся книг по автору"""
    book_count = session.query(func.sum(Book.count)).filter(Book.author_id == author_id).scalar()
    return jsonify(count=book_count), 200


@app.route('/students/debtors', methods=['GET'])
def get_students_debtors():
    """Получение списка студентов-должников, которые держат книгу более 14 дней"""
    debtors = (
        session.query(ReceivingBook).filter(ReceivingBook.date_of_issue < (datetime.now() - timedelta(days=14))).all())
    debtors_list = [debtor.to_json() for debtor in debtors]
    return jsonify(debtors_list=debtors_list), 200

@app.route('/books/recommend/<int:student_id>', methods=['GET'])
def recommend_book_to_student(student_id):
    """Получение списка книг, которые студент не читал, при этом другие книги этого автора студент уже брал"""
    authors_id = session.query(ReceivingBook.book_id).distinct().filter(ReceivingBook.student_id == student_id).subquery()
    books = session.query(Book).filter(Book.author_id in authors_id).all()
    books = [books.to_json() for books in books]
    return jsonify(books=books), 200


@app.route('/students/avg-count-book/', methods=['GET'])
def recommend_book_to_student(student_id):
    """Получение среднего количества книг, которые студенты брали в этом месяце"""
    books_count = session.query(func.count(ReceivingBook.id)).filter(extract('month', ReceivingBook.date_of_issue) == datetime.now().month).scalar()
    student_count = session.query(func.count(Student.id)).scalar()
    avg_count_books = books_count / student_count if student_count else 0
    return jsonify(average_count_books_per_month=avg_count_books), 200


@app.route('/book/issue', methods=['POST'])
def issue_book():
    """Добавление книги в таблицу выданных книг"""
    book_id = request.form.get('book_id', type=int)
    student_id = request.form.get('student_id', type=int)
    date_of_issue = request.form.get('date_of_issue', type=str)

    new_receiving_book = ReceivingBook(book_id=book_id,
                                       student_id=student_id,
                                       date_of_issue=datetime.strptime(date_of_issue, '%Y%m%d %H:%M:%S'))
    session.add(new_receiving_book)
    return "Книга добавлена в таблицу выданных книг", 201


@app.route('/book/return', methods=['POST'])
def return_book():
    """Обновление даты возвращения книги"""
    try:
        book_id = request.form.get('book_id', type=int)
        student_id = request.form.get('student_id', type=int)
        book = session.query(ReceivingBook).filter(ReceivingBook.book_id == book_id,
                                                   ReceivingBook.student_id == student_id).one()
        book.date_of_return = datetime.now()
        session.commit()
        return "Обновлена дата возвращения книги", 200
    except NoResultFound:
        return "Книгу с таким book_id и student_id не удалось найти"


@app.route('/books/popular', methods=['GET'])
def get_popular_book():
    """Получение самой популярной книгу среди студентов, у которых средний балл больше 4.0"""
    students = session.query(Student).filter(Student.average_score > 4.0).all()
    book_counts = {}
    for student in students:
        for book in student.books:
            book_counts[book.id] = book_counts.get(book.id, 0) + 1

    most_popular_book_id = max(book_counts, key=book_counts.get) if book_counts else None
    most_popular_book = session.query(Book).filter(Book.id == most_popular_book_id).first()

    return jsonify(most_popular_book=most_popular_book.to_json()), 200


@app.route('/students/top_readers', methods=['GET'])
def get_top_readers():
    """Получение ТОП-10 самых читающих студентов в этом году"""
    top_readers = session.query(Student).order_by(desc(Student.books_count)).limit(10).all()
    top_readers_list = [student.to_json() for student in top_readers]
    return jsonify(top_readers=top_readers_list)


if __name__ == "__main__":
    app.run(debug=True)

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, DateTime
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from flask import Flask, jsonify, request
from datetime import datetime, timedelta

app = Flask(__name__)

engine = create_engine("sqlite:///library.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def get_all_students_with_scholarship(cls):
        return session.query(Student).filter(Student.scholarship == True).all()

    @classmethod
    def get_students_by_average_score(cls, average_score: float):
        return session.query(Student).filter(Student.average_score > average_score).all()


class ReceivingBook(Base):
    __tablename__ = 'receiving_books'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)

    @hybrid_property
    def count_date_with_book(self):
        if self.date_of_return:
            return self.date_of_return - self.date_of_issue
        else:
            return datetime.now() - self.date_of_issue

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@app.before_request
def before_request_func():
    Base.metadata.create_all(engine)


@app.route('/books', methods=['GET'])
def all_books():
    """Получение списка всех книг"""
    books = session.query(Book).all()
    books_list = [book.to_json() for book in books]
    return jsonify(books_list=books_list), 200

@app.route('/books-r', methods=['GET'])
def all_books_r():
    """Получение списка всех книг"""
    books_r = session.query(ReceivingBook).all()
    books_list_r = [book.to_json() for book in books_r]
    return jsonify(books_list=books_list_r), 200


@app.route('/students-debtors', methods=['GET'])
def get_students_debtors():
    """Получение списка студентов-должников, которые держат книгу более 14 дней"""
    debtors = (session.query(ReceivingBook).filter(ReceivingBook.date_of_issue < (datetime.now() - timedelta(days=14))).all())

    debtors_list = [debtor.to_json() for debtor in debtors]
    return jsonify(debtors_list=debtors_list), 200


@app.route('/book-issue', methods=['POST'])
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


@app.route('/book-return', methods=['POST'])
def return_book():
    """Обновление даты возвращения книги"""
    try:
        book_id = request.form.get('book_id', type=int)
        student_id = request.form.get('student_id', type=int)
        book = session.query(ReceivingBook).filter(ReceivingBook.book_id == book_id, ReceivingBook.student_id == student_id).one()
        book.date_of_return = datetime.now()
        session.commit()
        return "Обновлена дата возвращения книги", 200
    except NoResultFound:
        return "Книгу с таким book_id и student_id не удалось найти"


if __name__ == "__main__":
    app.run(debug=True)

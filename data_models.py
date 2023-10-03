from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = "authors"
    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.String, nullable=False)
    date_of_death = db.Column(db.String)

    def __init__(self, author_name, birth_date, date_of_death):
        self.author_name = author_name
        self.birth_date = birth_date
        self.date_of_death = date_of_death

class Book(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.Integer, unique=True)
    title = db.Column(db.String)
    publication_year = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.author_id"))


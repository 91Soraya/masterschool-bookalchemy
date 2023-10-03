from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from sqlalchemy import select, or_
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.root_path}\data\library.sqlite"
db.init_app(app)

#with app.app_context():
#    db.create_all()

@app.route("/")
def hello():
    return redirect(url_for("home"))


@app.route("/home", methods=["GET", "POST"])
def home():
    books = Book.query.all()
    authors = Author.query.all()
    sort_by = request.form.get("sort_by")

    if sort_by == "title_asc":
        books = Book.query.order_by(Book.title)
    if sort_by == "title_desc":
        books = Book.query.order_by(Book.title.desc())
    if sort_by == "author_asc":
        books = Book.query.join(Author).order_by(Author.author_name)
    if sort_by == "author_desc":
        books = Book.query.join(Author).order_by(Author.author_name.desc())


    search_for = request.form.get("search_for")
    if search_for:
        books = Book.query.join(Author).filter(or_(Book.title.like("%"+search_for+"%"), Author.author_name.like("%"+search_for+"%")))
        num_of_books_found = 0
        for book in books:
            num_of_books_found += 1
        if num_of_books_found == 0:
            message = "Not found"
            return render_template("home.html", books=books, authors=authors, message=message)

    return render_template("home.html", books=books, authors=authors)




@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        author_name = request.form.get("name")
        birth_date = request.form.get("birthdate")
        date_of_death = request.form.get("date_of_death")

        new_author = Author(author_name=author_name, birth_date=birth_date, date_of_death=date_of_death)

        db.session.add(new_author)
        db.session.commit()

        return f"Author {new_author.author_name} added with author id {new_author.author_id}"

    return render_template("add_author.html")


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    all_authors = Author.query.all()
    if request.method == "POST":
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        publication_year = request.form.get("publication_year")
        author_id = request.form.get("author")

        new_book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id)

        db.session.add(new_book)
        db.session.commit()

        return f"Book {new_book.title} added with book id {new_book.book_id}"

    return render_template("add_book.html", all_authors=all_authors)

@app.route("/book/<int:book_id>/delete", methods=["GET", "POST"])
def delete_book(book_id):
    if request.method == "POST":
        id_to_delete = book_id
        Book.query.filter(Book.book_id == id_to_delete).delete()
        db.session.delete()
        return f"Book has been deleted."
    return redirect("/home")

if __name__ == "__main__":
    app.run(debug=True)
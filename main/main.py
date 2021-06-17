from types import MethodDescriptorType
from flask import Blueprint, render_template, request, redirect
from . import db
from flask_login import login_required, current_user
from .models import Book

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@main.route('/add', methods=['POST', 'GET'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        url = request.form.get('url')
        topic = request.form.get('topic')
        summary = request.form.get('summary')
        new_book = Book(title=title,author=author,url=url,topic=topic,summary=summary)
        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect(request.referrer)
        except:
            return "There was an issue adding your book"
    else:
        return render_template('add.html')    

@main.route('/delete/<int:id>')
def delete(id):
    book_to_delete = Book.query.get_or_404(id)
    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect(request.referrer)
    
    except:
        return "There was a problem deleting your task"

@main.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    book_to_update = Book.query.get_or_404(id)
    if request.method == 'POST':
        book_to_update.title = request.form['title']
        book_to_update.author = request.form['author']
        book_to_update.url= request.form['url']
        book_to_update.topic = request.form['topic']
        book_to_update.summary = request.form['summary']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating your task "
    else:
        return render_template("update.html", book=book_to_update)

@main.route('/book/<int:id>')
def book(id):
    book = Book.query.get_or_404(id)
    return render_template("book.html", book=book)

@main.route('/all')
def all():
    books = Book.query.order_by(Book.date_created).all()
    return render_template('search.html', books=books)

@main.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search']
        search = "%{}%".format(search_value)
        books = Book.query.filter(Book.title.like(search)).all()
        return render_template('search.html', books=books)

@main.route('/filter/<string:topic>')
def filter(topic):
    form = request.form
    books = Book.query.filter_by(topic=topic).all()
    return render_template('search.html', books=books)



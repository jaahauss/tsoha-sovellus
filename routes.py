from app import app
from flask import redirect, render_template, request, session
import users, archiving, suggestions
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from db import db

@app.route("/")
def index():
    sql = "SELECT id, topic, created_at FROM books WHERE visible=TRUE ORDER BY id DESC"
    result = db.session.execute(text(sql))
    books = result.fetchall()
    sql = "SELECT id, content FROM suggestions ORDER BY id DESC"
    result = db.session.execute(text(sql))
    suggestions = result.fetchall()
    return render_template("index.html", books=books, suggestions=suggestions)
    
@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/new_suggestion")
def new_suggestion():
    return render_template("new_suggestion.html")
    
@app.route("/create", methods=["POST"])
def create():
    topic = request.form["topic"]
    sql = text("INSERT INTO books (topic, created_at) VALUES (:topic, NOW()) RETURNING id")
    result = db.session.execute(sql, {"topic":topic})
    book_id = result.fetchone()[0]
    sql = text("UPDATE books SET visible=TRUE WHERE id=:book_id")
    db.session.execute(sql, {"book_id":book_id})
    db.session.commit()
    return redirect("/")

@app.route("/write/<int:id>")
def write(id):
    sql = text("SELECT topic FROM books WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    return render_template("new_message.html", id=id, topic=topic)

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    book_id = request.form["id"]
    sql = text("INSERT INTO messages (book_id, content) VALUES (:book_id, :content)")
    db.session.execute(sql, {"book_id":book_id, "content":content})
    db.session.commit()
    return redirect("/")
    
@app.route("/result/<int:id>")
def result(id):
    sql = text("SELECT topic FROM books WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    sql = text("SELECT m.content FROM messages m WHERE m.book_id=:book_id")
    result = db.session.execute(sql, {"book_id":id})
    messages = result.fetchall()
    return render_template("result.html", topic=topic, messages=messages)

@app.route("/archive/<int:id>")
def archive(id):
    archiving.archive(id)
    return redirect("/")

@app.route("/archive_result")
def archive_result():
    books = archiving.archive_result()
    return render_template("archive_result.html", books=books)

@app.route("/unarchive/<int:id>")
def unarchive(id):
    archiving.unarchive(id)
    return redirect("/")

@app.route("/suggest", methods=["POST"])
def suggest():
    content = request.form["content"]
    suggestions.suggest(content)
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        session["username"] = username
        return redirect("/")
    else:
        return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

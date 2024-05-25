from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = "SELECT id, topic, created_at FROM books ORDER BY id DESC"
    result = db.session.execute(text(sql))
    books = result.fetchall()
    return render_template("index.html", books=books)
    
@app.route("/new")
def new():
    return render_template("new.html")
    
@app.route("/create", methods=["POST"])
def create():
    topic = request.form["topic"]
    sql = text("INSERT INTO books (topic, created_at) VALUES (:topic, NOW()) RETURNING id")
    result = db.session.execute(sql, {"topic":topic})
    book_id = result.fetchone()[0]
    db.session.commit()
    return redirect("/")

@app.route("/book/<int:id>")
def book(id):
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

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


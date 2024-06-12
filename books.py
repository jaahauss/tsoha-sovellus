from db import db
from flask import session
from sqlalchemy.sql import text

def index(user_id):
    sql = text("SELECT admin FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    is_admin = result.fetchone()[0]
    sql = "SELECT b.id, b.topic, b.created_at, SUM(r.grade), COUNT(r.grade) FROM books b LEFT JOIN reviews r ON b.id=r.book_id WHERE b.visible=TRUE GROUP BY b.id ORDER BY b.id DESC"
    result = db.session.execute(text(sql))
    books = result.fetchall()
    sql = "SELECT id, content FROM suggestions WHERE visible=TRUE ORDER BY id DESC"
    result = db.session.execute(text(sql))
    suggestions = result.fetchall()
    return [books, suggestions, is_admin]

def create(topic):
    sql = text("INSERT INTO books (topic, created_at) VALUES (:topic, NOW()) RETURNING id")
    result = db.session.execute(sql, {"topic":topic})
    book_id = result.fetchone()[0]
    sql = text("UPDATE books SET visible=TRUE WHERE id=:book_id")
    db.session.execute(sql, {"book_id":book_id})
    db.session.commit()


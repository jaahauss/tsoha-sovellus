from db import db
from flask import session
from sqlalchemy.sql import text

def index(user_id):
    sql = text("SELECT admin FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    is_admin = result.fetchone()[0]
    sql = "SELECT books.id, books.topic, books.created_at, sub1.gradesum, sub1.gradecount, sub2.messagecount FROM books LEFT OUTER JOIN (SELECT book_id, SUM(grade) AS gradesum, COUNT(grade) AS gradecount FROM reviews GROUP BY book_id) AS sub1 ON sub1.book_id=books.id LEFT OUTER JOIN (SELECT book_id, COUNT(id) AS messagecount FROM messages WHERE visible=TRUE GROUP BY book_id) AS sub2 ON sub2.book_id=books.id WHERE books.visible=TRUE ORDER BY books.created_at DESC"
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


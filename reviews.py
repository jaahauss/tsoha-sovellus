from db import db
from flask import session
from sqlalchemy.sql import text

def review(id):
    sql = text("SELECT topic FROM books WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    return topic

def send(grade, book_id):
    sql = text("INSERT INTO reviews (book_id, grade) VALUES (:book_id, :grade)")
    db.session.execute(sql, {"book_id":book_id, "grade":grade})
    db.session.commit()

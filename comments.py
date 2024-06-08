from db import db
from flask import session
from sqlalchemy.sql import text

def write(id):
    sql = text("SELECT topic FROM books WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    return topic

def send(user_id, content, book_id):
    sql = text("INSERT INTO messages (book_id, content, user_id) VALUES (:book_id, :content, :user_id)")
    db.session.execute(sql, {"book_id":book_id, "content":content, "user_id":user_id})
    db.session.commit()

def result(user_id, id):
    sql = text("SELECT username FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    user_name = result.fetchone()[0]
    sql = text("SELECT admin FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    is_admin = result.fetchone()[0]
    sql = text("SELECT topic FROM books WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    sql = text("SELECT m.content, u.username FROM messages m, users u WHERE m.book_id=:book_id AND m.user_id=u.id")
    result = db.session.execute(sql, {"book_id":id})
    messages = result.fetchall()
    return [topic, messages, user_name, is_admin]

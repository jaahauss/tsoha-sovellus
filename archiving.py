from db import db
from flask import session
from sqlalchemy.sql import text

def archive(id):
    sql = text("UPDATE books SET visible=FALSE WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()

def archive_index():
    sql = "SELECT id, topic, created_at FROM books WHERE visible=FALSE ORDER BY id DESC"
    result = db.session.execute(text(sql))
    books = result.fetchall()
    return books

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
    sql = text("SELECT m.id, m.content, u.username FROM messages m, users u WHERE m.book_id=:book_id AND m.user_id=u.id AND m.visible=TRUE")
    result = db.session.execute(sql, {"book_id":id})
    messages = result.fetchall()
    return [topic, messages, user_name, is_admin]


def unarchive(id):
    sql = text("UPDATE books SET visible=TRUE WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()

from db import db
from flask import session
from sqlalchemy.sql import text

def write(id):
    sql = text("SELECT topic FROM books WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    return topic

def send(user_id, content, book_id):
    sql = text("INSERT INTO messages (book_id, content, user_id) VALUES (:book_id, :content, :user_id) RETURNING id")
    result = db.session.execute(sql, {"book_id":book_id, "content":content, "user_id":user_id})
    message_id = result.fetchone()[0]
    sql = text("UPDATE messages SET visible=TRUE WHERE id=:message_id")
    db.session.execute(sql, {"message_id":message_id})
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
    sql = text("SELECT m.id, m.content, u.username FROM messages m, users u WHERE m.book_id=:book_id AND m.user_id=u.id AND m.visible=TRUE")
    result = db.session.execute(sql, {"book_id":id})
    messages = result.fetchall()
    return [topic, messages, user_name, is_admin]

def delete(id):
    sql = text("UPDATE messages SET visible=FALSE WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()

def alter(book_id):
    sql = text("SELECT topic FROM books WHERE id=:book_id")
    result = db.session.execute(sql, {"book_id":book_id})
    topic = result.fetchone()[0]
    return topic

def send_altered(content, message_id):
    sql = text("UPDATE messages SET content=:content WHERE id=:message_id")
    db.session.execute(sql, {"content":content, "message_id":message_id})
    db.session.commit()

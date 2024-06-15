from db import db
from flask import session
from sqlalchemy.sql import text

def archive(id):
    sql = text("UPDATE books SET visible=FALSE WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()

def archive_index():
    sql = "SELECT id, topic, created_at FROM books WHERE visible=FALSE ORDER BY created_at DESC"
    result = db.session.execute(text(sql))
    books = result.fetchall()
    return books

def unarchive(id):
    sql = text("UPDATE books SET visible=TRUE WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()

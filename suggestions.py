from db import db
from flask import session
from sqlalchemy.sql import text

def suggest(content):
    sql = text("INSERT INTO suggestions (content) VALUES (:content) RETURNING id")
    result = db.session.execute(sql, {"content":content})
    suggestion_id = result.fetchone()[0]
    sql = text("UPDATE suggestions SET visible=TRUE WHERE id=:suggestion_id")
    db.session.execute(sql, {"suggestion_id":suggestion_id})
    db.session.commit()
    
def delete(id):
    sql = text("UPDATE suggestions SET visible=FALSE WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()

def approve(id):
    sql = text("UPDATE suggestions SET visible=FALSE WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    sql = text("SELECT content FROM suggestions WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()[0]
    sql = text("INSERT INTO books (topic, created_at) VALUES (:topic, NOW()) RETURNING id")
    result = db.session.execute(sql, {"topic":topic})
    book_id = result.fetchone()[0]
    sql = text("UPDATE books SET visible=TRUE WHERE id=:book_id")
    db.session.execute(sql, {"book_id":book_id})
    db.session.commit()


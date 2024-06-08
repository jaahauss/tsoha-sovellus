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


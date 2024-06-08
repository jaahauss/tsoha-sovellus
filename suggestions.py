from db import db
from flask import session
from sqlalchemy.sql import text

def suggest(content):
    sql = text("INSERT INTO suggestions (content) VALUES (:content)")
    db.session.execute(sql, {"content":content})
    sql = text("UPDATE suggestions SET visible=TRUE WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    
def delete(id):
    sql = text("UPDATE suggestions SET visible=FALSE WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()


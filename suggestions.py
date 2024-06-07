from db import db
from flask import session
from sqlalchemy.sql import text

def suggest(content):
    sql = text("INSERT INTO suggestions (content) VALUES (:content)")
    db.session.execute(sql, {"content":content})
    db.session.commit()

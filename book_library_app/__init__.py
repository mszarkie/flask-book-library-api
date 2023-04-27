from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from sqlalchemy.sql import text

app = Flask(__name__)
app.config.from_object(Config)

app_ctx = app.app_context()
app_ctx.push()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# results = db.session.execute(text('show databases'))
# for row in results:
#     print(row)
# /\ testowanie czy udało się podłączyć do bazy danych MySQL

from book_library_app import authors
from book_library_app import models
from book_library_app import db_meange_commands
from book_library_app import errors

import json
from pathlib import Path
from datetime import datetime

from book_library_app import db
from book_library_app.models import Author
from book_library_app.commands import db_menage_bp
from sqlalchemy.sql import text


@db_menage_bp.cli.group()
def db_menage():
    """Database management commands"""
    pass


@db_menage.command()
def add_data():
    """Add sampledata to database"""
    try:
        authors_path = Path(__file__).parent.parent / 'samples' / 'authors.json'
        with open(authors_path) as file:
            data_json = json.load(file)
        for item in data_json:
            item['birth_date'] = datetime.strptime(item['birth_date'], '%d-%m-%Y').date()
            author = Author(**item)
            db.session.add(author)
        db.session.commit()
        print('Data has neem successfully added to database')
    except Exception as exc:
        print("Unexpected error: {}".format(exc))


@db_menage.command()
def remove_data():
    """Remove all data from the database"""
    try:
       db.session.execute(text(('TRUNCATE TABLE authors')))
       db.session.commit()
       print('Data has been successfully removed from database')
    except Exception as exc:
        print("Unexpected error: {}".format(exc))

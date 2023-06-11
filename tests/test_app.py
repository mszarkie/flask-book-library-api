from flask import Flask
from book_library_app import db


def test_app(app):
    assert isinstance(app, Flask)
    assert app.config['TESTING'] is True
    assert app.config['DEBUG'] is True

    with app.app_context():
        db.engine.dispose()

from flask import Blueprint

error_bp = Blueprint('errors', __name__)

from book_library_app.errors import errors
from flask import Blueprint

db_menage_bp = Blueprint('db_menage_cmd', __name__, cli_group=None)

from book_library_app.commands import db_meange_commands


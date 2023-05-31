from book_library_app import db
from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime, date


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    books = db.relationship('Book', back_populates='Author', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.first_name} {self.last_name}'

    @staticmethod
    def additional_validation(param: str, value: str) -> date:
        if param == 'birth_date':
            try:
                value = datetime.strptime(value, '%d-%m-%Y').date()
            except ValueError:
                value = None
        return value

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    isbn = db.Column(db.BigInteger, nullable=False, unique=True)
    number_of_pages = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    Author = db.relationship('Author', back_populates='books')

    def __repr__(self):
        return f'{self.title} - {self.author.first_name} {self.author.last_name}'

    @staticmethod
    def additional_validation(param: str, value: str) -> str:
        return value

class AuthorSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True, validate=validate.Length(max=50))
    last_name = fields.String(required=True, validate=validate.Length(max=50))
    birth_date = fields.Date('%d-%m-%Y', required=True)
    books = fields.List(fields.Nested(lambda: BookSchema(exclude=['author'])))

    @validates('birth_date')
    def validate_birth_date(self, value):
        if value > datetime.now().date():
            raise ValidationError(f'Birth date must be lower than {datetime.now().date()}')


class BookSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(max=50))
    isbn = fields.Integer(required=True)
    number_of_pages = fields.Integer(required=True)
    description = fields.String()
    author_id = fields.Integer(load_only=True)
    Author = fields.Nested(lambda: AuthorSchema(only=['id', 'first_name', 'last_name']))

    @validates('isbn')
    def validate_isbn(self, value):
        if len(str(value)) != 13:
            raise ValidationError('ISBN must contains 13 digits')


autor_schema = AuthorSchema()
book_schema = BookSchema()

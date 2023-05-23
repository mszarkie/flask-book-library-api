from book_library_app import app, db
from webargs.flaskparser import use_args
from flask import jsonify, request
from book_library_app.models import Author, AuthorSchema, autor_schema
from book_library_app.utils import validate_json_content_type


@app.route('/api/v1/authors', methods=['GET'])
def get_authors():
    query = Author.query
    schema_args = Author.get_schema_args(request.args.get('fields'))
    query = Author.apply_order(query, request.args.get('sort'))
    query = Author.apply_filter(query)
    items, pagination = Author.get_pagination(query)

    authors = AuthorSchema(**schema_args).dump(items)

    return jsonify({
        'success': True,
        'data': authors,
        'number_of_records': len(authors),
        'pagination': pagination
    })


@app.route('/api/v1/authors/<int:author_id>', methods=['GET'])
def get_author(author_id: int):
    author = Author.query.get_or_404(author_id, description=f'Author with id {author_id} not found')
    return jsonify({
        'success' : True,
        'data' : autor_schema.dump(author)
    })


@app.route('/api/v1/authors', methods=['POST'])
@validate_json_content_type
@use_args(autor_schema, error_status_code=400)
def create_author(args: dict):
    author = Author(**args)

    db.session.add(author)
    db.session.commit()
    return jsonify({
        'success' : True,
        'data' : autor_schema.dump(author)
    }), 201


@app.route('/api/v1/authors/<int:author_id>', methods=['PUT'])
@validate_json_content_type
@use_args(autor_schema, error_status_code=400)
def update_author(args: dict, author_id: int):
    author = Author.query.get_or_404(author_id, description=f'Author with id {author_id} not found')

    author.first_name = args['first_name']
    author.last_name = args['last_name']
    author.birth_date = args['birth_date']

    db.session.commit()

    return jsonify({
        'success' : True,
        'data' : autor_schema.dump(author)
    })


@app.route('/api/v1/authors/<int:author_id>', methods=['DELETE'])
def delete_author(author_id: int):
    author = Author.query.get_or_404(author_id, description=f'Author with id {author_id} not found')

    db.session.delete(author)
    db.session.commit()

    return jsonify({
        'success' : True,
        'data' : f'Author with id {author_id} has been deleted'
    })
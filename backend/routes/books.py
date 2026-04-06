from flask import Blueprint, request, jsonify
from db import get_connection

book_routes = Blueprint('books', __name__)


#sselect all books
@book_routes.route('/', methods=['GET'])
def get_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM BOOKS")
    books = cursor.fetchall()

    results = []
    for book in books:
        results.append({
            "id": book.BOOK_ID,
            "title": book.TITLE,
            "price": float(book.PRICE),
            "stock": book.STOCK
        })
    
    conn.close()
    
    return jsonify(results)


#select one book
@book_routes.route('/<int:id>', method=['GET'])
def get_book(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM BOOKS WHERE BOOK_ID = ?", (id,))
    book = cursor.fetchone()

    if not book:
        return jsonify ({"error": "Book not found"}, 404)
    
    return{
        "id": book.BOOK_ID,
        "title": book.TITLE,
        "price": float(book.PRICE),
        "stock": book.STOCK
    }


#add book
@book_routes.route('/', methods=['POST'])
def add_book():
    data = request.json

    title = data['title']
    author = data['author']
    price = data['price']
    stock = data['stock']
    description = data.get('description', '')
    image_url = data.get('image_url', '')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO BOOKS (BOOK_TITLE, AUTHOR, PRICE, STOCK, DESCRIPTION, IMAGE_URL) VALUES (?, ?, ?, ?, ?, ?)",
        (title, author, price, stock, description, image_url)
    )

    conn.commit()
    conn.close()

    return jsonify ({"message": "Book added successfully"})


#update book
@book_routes.route('/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE BOOKS SET TITLE=?, AUTHOR=?, PRICE=?, STOCK=? WHERE BOOK_ID=?",
        (data['title'], data['author'], data['price'], data['stock'], id) 
    )

    conn.commit()
    conn.close()

    return jsonify ({"message": "Book updated"})


#delete book
@book_routes.route('/<int:id>', method=['DELETE'])
def delete_book(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM BOOKS WHERE BOOK_ID=?", (id,))

    conn.commit()
    conn.close()

    return jsonify ({"message": "Book deleted succesfully"})


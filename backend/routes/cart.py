from flask import Blueprint, jsonify, request, session
from db import get_connection

cart_route = Blueprint('cart', __name__)

"""
#check if a user is logged in
def get_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return user_id
    """

#add to cart
@cart_route.route('/add', methods=['POST'])
def add_to_cart():
    user_id = session.get_user()
    if not user_id:
        return jsonify ({"error": "Unauthorized"}), 401
    
    data = request.json

    book_id = data['book_id']
    quantity = data.get('quantity', 1)

    conn = get_connection()
    cursor = conn.cursor()

    #check if the item already in cart 
    cursor.execute(
        "SELECT * FROM CART WHERE USER_ID=? AND BOOK_ID=?",
        (user_id, book_id)
    )

    item = cursor.fetchone()

    if item:
        cursor.execute(
            "UPDATE CART SET QUANTITY = QUANTITY + ? WHERE CART_ID=?",
            (quantity, item.id)
        )
    else:
        cursor.execute(
            "INSERT INTO CART (USER_ID, BOOK_ID, QUANTITY) VALUES (?,?,?)",
            (user_id, book_id, quantity)
        )

    conn.commit()
    conn.close()

    return jsonify ({"message": "Added to cart"})

#view cart
@cart_route.route('/', methods=['GET'])
def view_cart():
    user_id = session.get_user()
    if not user_id:
        return jsonify ({"error": "Unauthorized"}), 401
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT CART.CART_ID, BOOKS.TITLE, BOOKS.PRICE, CART.QUANTITY FROM CART JOIN BOOKS ON CART.BOOK_ID = BOOKS.BOOK_ID WHERE CART.USER_ID=?",
        (user_id,)
    )

    items = cursor.fetchall()

    results = []

    for item in items:
        results.append({
            "cart_id": item.id,
            "title": item.title,
            "price": float(item.price),
            "quantity": item.quantity
        })

    conn.close()
    return results

#remove item
@cart_route.route('/<int:id>', methods=['DELETE'])
def remove_item(id):
    user_id = session.get_user()
    if not user_id:
        return jsonify ({"error": "Unauthorized"}), 401
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM CART WHERE CART_ID=? AND USER_ID=?",
        (id, user_id)
    )

    conn.commit()
    conn.close()

    return jsonify ({"message": "Item removed"})
    

#update cart
@cart_route.route('<int:id>', methods=['PUT'])
def update_quantity(id):
    user_id = session.get_user()
    if not user_id:
        return jsonify ({"error": "User not found"})
    
    data = request.json
    quantity = data['quantity']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE CART SET QUANTITY=? WHERE CART_ID=? AND USER_ID=?",
        (quantity, id, user_id)
    )

    conn.commit()
    conn.close()

    return jsonify ({"Message": "Cart updated"})


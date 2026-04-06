from flask import session, jsonify, Blueprint
from db import get_connection

order_routes = Blueprint('orders', __name__)

#checkout
@order_routes.route('/checkout', methods=['POST'])
def checkout():
    user_id = session.get_user()
    if not user_id:
        return jsonify ({"error": "Unauthorized"}), 401
    
    conn = get_connection()
    cursor = conn.cursor()

    #get cart items
    cursor.execute(
        "SELECT CART.BOOK_ID, CART.QUANTITY, BOOKS.PRICE, BOOKS.STOCK FROM CART JOIN BOOKS ON CART.BOOK_ID = BOOK.BOOK_ID WHERE CART.USER_ID=?",
        (user_id,)
    )

    items = cursor.fetchall()

    if not items:
        return jsonify ({"error": "cart is empty"}), 400
    
    total_price = 0

    #calculate total price
    for item in items:
        if item.quantity > item.stock:
            return jsonify ({"error": f"not enough stock for book {item.book_id}"})
        
        total_price += item.quantity * float(item.price)

    #create order
    cursor.execute(
        "INSERT INTO ORDERS (USER_ID, TOTAL_PRICE) OUTPUT INSERTED.ORDER_ID VALUES (?, ?)",
        (user_id, total_price)
    )

    order_id = cursor.fetchone()

    # insert order items and reduce stock
    for item in items:
        cursor.execute(
            "INSERT INTO ORDER_ITEMS (ORDER_ITEM_ID, BOOK_ID, 'QUANTITY', 'PRICE') VALUES (?, ?, ?, ?)",
            (order_id, item.book_id, item.quantity, item.price)
        )

        cursor.execute(
            "UPDATE BOOKS SET STOCK = STOCK - ? WHERE BOOK_ID = ?",
            (item.quantity, item.book_id)
        )

    #clear cart
    cursor.execute(
        "DELETE FROM CART WHERE USER_ID = ?",
        (user_id,)   
    )

    conn.commit()
    conn.close()

    return jsonify ({
        "message": "Order placed succesfully",
        "order_id": order_id,
        "total": total_price
    })


# view user orders
@order_routes.route('/', methods=['GET'])
def get_orders():
    user_id = session.get_user()
    if not user_id:
        return jsonify ({"error": "Unauthorized"}), 401
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT ORDER_ID, TOTAL_PRICE, STATUS, CREATED_AT FROM ORDERS WHERE USER_ID =?",
        (user_id,)
    )

    orders = cursor.fetchall()

    results = []
    for order in orders:
        results.append({
            "order_id": order.order_id,
            "total": float(order.total_price),
            "status": order.status,
            "date": str(order.created_at)
        })

    conn.close()
    
    return results


@order_routes.route('/<int:order_id>', methods = "GET")
def order_details(order_id):
    user_id = session.get_user()
    if not user:
        return jsonify ({"error": "Unauthorized"}), 401
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT BOOKS.TITLE, ORDER_ITEMS.QUANTITY, ORDER_ITEMS.PRICE FROM ORDER_ITEMS JOIN BOOKS ON ORDER_ITEMS.BOOK_ID = BOOKS.BOOK_ID WHERE ORDER_ITEMS.ORDER_ID=?",
        (order_id,)
    )

    items = cursor.fetchall()

    results = []
    for item in items:
        results.append({
            "title": item.title,
            "quantity": item.quantity,
            "price": float(item.price)
        })

    conn.close()

    return results




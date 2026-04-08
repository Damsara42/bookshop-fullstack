async function addToCart(bookId) {
    await fetch('http://127.0.0.1:5000/cart/add', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        credentials: 'include', 
        body: JSON.stringify({
            book_id: bookId,
            quantity: 1
        })
    });

    alert ("Added to cart");
}

async function loadCart() {
    const res = await fetch('https://127.0.0.1:5000/cart/', {
        credentials: 'include'
    });

    const items = await res.json();

    const container = document.getElementById('cart');
    container.innerHTML = '';

    items.forEach(item => {
        container.innerHTML += `
           <div>
             <h3>${item.title}</h3>
             <p>${item.quantity} x Rs. ${item.price}</p>
             <button onclick="removeItem(${item.cart_id})">Remove</button>
            </div>
        `;
    });
}

async function removeItem(id) {
    await fetch('http://127.0.0.1:5000/cart/${id}', {
        method: 'DELETE',
        credentials: 'include'
    });

    loadCart();
}

async function checkout() {
    const res = await fetch('http://127.0.0.1:5000/orders/checkout', {
        method: 'POST',
        credentials: 'include'
    });

    const data = await res.json();

    if (res.ok) {
        alert("Order placed");
        loadCart();
    }
    else {
        alert(data.error);
    }
}

loadCart();
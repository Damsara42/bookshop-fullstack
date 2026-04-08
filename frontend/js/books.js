async function loadBooks() {
    const res = await fetch('http://127.0.0.1:5000/books/');
    const books = await res.json();

    const container = document.getElementById('books');
    container.innerHTML = '';

    books.forEach(book => {
        container.innerHTML += ` # let u mix HTML strings with js variables easily
            <div>
                <h3>${book.title}</h3>
                <p>${book.author}</p>
                <p>Rs. ${book.price}</p>
                <button onclick="addToCart(${book.id})">Add to cart</button>
            </div>
        `;

    });

}

loadBooks();

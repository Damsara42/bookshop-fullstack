async function login() {
    const email = document.getElementById('email').value;
    const password = documet.getElementById('passowrd').value;

    const res = await fetch('http://127.0.0.1:5000/auth/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        credentials: 'include',
        body: JSON.stringify({email,password})
    });

    const data = await res.json();

    if (res.ok) {
        alert("Login success")
        window.location.href = "index.html";
    }
    else {
        alert(data.error);
    }
}
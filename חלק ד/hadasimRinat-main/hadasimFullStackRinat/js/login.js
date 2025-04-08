function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            localStorage.setItem("supplierName", String(username)); 
            window.location.href = 'dashboard.html';
        } else if (data.redirect) {
            window.location.href = 'regist.html';
        } else {
            document.getElementById('error-msg').textContent = 'שם משתמש או סיסמה שגויים';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}




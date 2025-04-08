function registerUser(event) {
    event.preventDefault(); 

    const data = {
        company: document.getElementById('company').value,
        phone: document.getElementById('phone').value,
        representative: document.getElementById('representative').value,
        products: document.getElementById('products').value,
        password: document.getElementById('password').value,
        name:document.getElementById('name').value
    };

    fetch('http://127.0.0.1:5000/regist', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(responseData => {
        if (responseData.success) {
            alert("ההרשמה בוצעה בהצלחה!");
            window.location.href = "login.html";  
            alert("שגיאה ברישום");
        }
    })
    .catch(error => {
        console.error("שגיאה בנתונים", error);
    });
}

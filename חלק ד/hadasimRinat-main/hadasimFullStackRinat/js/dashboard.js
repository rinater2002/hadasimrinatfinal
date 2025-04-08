// טעינת הזמנות ממתינות לאישור
function loadPendingOrders(orders) {
    const ordersList = document.getElementById("ordersList");
    if (!ordersList) {
        console.error('לא נמצא האלמנט ordersList בדף');
        return;
    }

    ordersList.innerHTML = ''; 
    Object.keys(orders).forEach(orderId => {
        const order = orders[orderId];

        const orderDiv = document.createElement("div");
        orderDiv.classList.add("order");

        const supplier = document.createElement("h3");
        supplier.textContent = `ספק: ${order.supplier}`;
        orderDiv.appendChild(supplier);

        const productList = document.createElement("ul");
        order.products.forEach(product => {
            const li = document.createElement("li");
            li.textContent = product;
            productList.appendChild(li);
        });
        orderDiv.appendChild(productList);

        const approveButton = document.createElement("button");
        approveButton.textContent = "אשר הזמנה";
        approveButton.onclick = () => approveOrder(order._id);
        orderDiv.appendChild(approveButton);

        ordersList.appendChild(orderDiv);
    });
}

// פונקציה לאשר הזמנה
function approveOrder(orderId) {
    fetch('http://127.0.0.1:5000/approve_order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order_id: orderId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("ההזמנה אושרה בהצלחה");
            loadPendingOrders(); // רענן את רשימת ההזמנות הממתינות
        } else {
            alert("לא ניתן לאשר את ההזמנה");
        }
    })
    .catch(error => console.error('Error approving order:', error));
}

// פונקציה לאשר הזמנה
function approveOrder(orderId) {
    fetch('http://127.0.0.1:5000/approve_order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order_id: orderId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("ההזמנה אושרה בהצלחה");
            window.location.reload();
        } else {
            alert("לא ניתן לאשר את ההזמנה");
        }
    })
    .catch(error => console.error('Error approving order:', error));
}

// טוען את ההזמנות הממתינות בזמן טעינת הדף
window.onload = function () {
    const supplierName = localStorage.getItem("supplierName");
    const encodedSupplierName = encodeURIComponent(supplierName);

    fetch(`http://127.0.0.1:5000/get_pending_orders?supplier=${encodedSupplierName}`)
        .then(response => response.json())
        .then(data => {
            loadPendingOrders(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
};
